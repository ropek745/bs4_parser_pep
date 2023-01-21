from collections import defaultdict
import logging
import re
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from constants import (
    BASE_DIR, CONNECTION_ERROR_MESSAGE, DOWNLOAD_DIR, DOWNLOADS_URL,
    ERROR_MESSAGE_URL, EXPECTED_STATUS, HEADS_OF_WHATS_NEW_TABLE,
    HEADS_OF_LATEST_VERSIONS_TABLE, LATEST_VERSIONS_ERROR_MESSAGE,
    MAIN_DOC_URL, PEP_URL, PARSER_ARGS_MESSAGE, PROGRAMM_ERROR_MESSAGE,
    PARSER_FINISHED, PATTERN_FOR_PEP_PARSE, PATTERN_FOR_LATEST_VERSIONS,
    RESULT_DOWNLOAD_MESSAGE, START_PARSER_MESSAGE, UNEXPECTED_STATUS,
    WHATS_NEW_URL
)
from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import find_tag, get_soup


def whats_new(session):
    sections_by_python = get_soup(session, WHATS_NEW_URL).select(
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1'
    )
    logs = []
    results = [HEADS_OF_WHATS_NEW_TABLE, ]
    for section in tqdm(sections_by_python):
        version_link = urljoin(WHATS_NEW_URL, section.select('a')[0]['href'])
        try:
            soup = get_soup(session, version_link)
            results.append(
                (
                    version_link,
                    find_tag(soup, 'h1').text,
                    find_tag(soup, 'dl').text.replace('\n', ' '),
                )
            )
        except ConnectionError:
            logs.append(ERROR_MESSAGE_URL.format(url=version_link))
    for log in logs:
        logging.info(log)
    return results


def latest_versions(session):
    ul_tags = get_soup(session, MAIN_DOC_URL).select(
        'div.sphinxsidebarwrapper ul'
    )
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ValueError(LATEST_VERSIONS_ERROR_MESSAGE)
    results = [HEADS_OF_LATEST_VERSIONS_TABLE, ]
    for a_tag in a_tags:
        text_match = re.search(PATTERN_FOR_LATEST_VERSIONS, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (a_tag['href'], version, status)
        )
    return results


def download(session):
    soup = get_soup(session, DOWNLOADS_URL)
    pdf_a4_tag = soup.select_one('table.docutils td > a[href$="pdf-a4.zip"]')
    archive_url = urljoin(DOWNLOADS_URL, pdf_a4_tag['href'])
    filename = archive_url.split('/')[-1]
    download_dir = BASE_DIR / DOWNLOAD_DIR
    download_dir.mkdir(exist_ok=True)
    archive_path = download_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(RESULT_DOWNLOAD_MESSAGE.format(archive_path=archive_path))


def pep(session):
    logs = []
    statuses_count = defaultdict(int)
    for tr_tag in tqdm(
        get_soup(session, PEP_URL).select('#numerical-index tbody tr')
    ):
        pep_url = urljoin(PEP_URL, find_tag(tr_tag, 'a')['href'])
        try:
            status_pep = tr_tag.text.split()[0][1:]
            dl_tag = get_soup(session, pep_url).find(
                'dl', attrs={'class': 'rfc2822 field-list simple'}
            )
            tag_with_status = dl_tag.find_all(
                'dd', string=re.compile(PATTERN_FOR_PEP_PARSE)
            )
            for status in tag_with_status:
                status_page = status.text
                if status_page not in EXPECTED_STATUS[status_pep]:
                    logs.append(UNEXPECTED_STATUS.format(
                        link=pep_url,
                        status=status_page,
                        expected_status=EXPECTED_STATUS[status_pep]
                    ))
            statuses_count[status_page] += 1
        except ConnectionError:
            logs.append(CONNECTION_ERROR_MESSAGE.format(url=pep_url))
    for log in logs:
        logging.info(log)
    return [
        ('Статус', 'Количество', ),
        *statuses_count.items(),
        ('Total', sum(statuses_count.values()))
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info(START_PARSER_MESSAGE)
    args = configure_argument_parser(MODE_TO_FUNCTION.keys()).parse_args()
    logging.info(PARSER_ARGS_MESSAGE.format(args=args))
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results:
            control_output(results, args)
    except Exception as error:
        logging.exception(
            PROGRAMM_ERROR_MESSAGE.format(error=error), stack_info=True
        )
    logging.info(PARSER_FINISHED)


if __name__ == '__main__':
    main()
