import csv
import re
from urllib.parse import urljoin
import logging

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from constants import (
    BASE_DIR, MAIN_DOC_URL, PEP_URL,
    EXPECTED_STATUS, STATUS_COUNT,
    UNEXPECTED_STATUS, PATTERN
)
from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import get_response, find_tag


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(soup, 'div', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        version_link = urljoin(whats_new_url, version_a_tag['href'])
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )

    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Не найден список c версиями Python')
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    div = find_tag(soup, 'div', attrs={'class': 'main'})
    table = find_tag(div, 'table', attrs={'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table, 'a', attrs={'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    pattern = PATTERN
    response = session.get(PEP_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    section_tag = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    tbody_tag = find_tag(section_tag, 'tbody')
    tr_tags = tbody_tag.find_all('tr')
    for tr_tag in tr_tags:
        status_in_pep_list = tr_tag.text.split()[0]
        link = find_tag(tr_tag, 'a')['href']
        pep_url = urljoin(PEP_URL, link)
        response = session.get(pep_url)
        pep_page = BeautifulSoup(response.text, 'lxml')
        dl_tag = pep_page.find(
            'dl', attrs={'class': 'rfc2822 field-list simple'}
        )
        tag_with_status = dl_tag.find_all('dd', string=re.compile(pattern))
        for status in tag_with_status:
            status_text = status.text
            if len(status_in_pep_list) == 1:
                STATUS_COUNT[status_text] += 1
            else:
                status_in_list = status_in_pep_list[1]
                if status_text in EXPECTED_STATUS[status_in_list]:
                    STATUS_COUNT[status_text] += 1
                else:
                    logging.info(UNEXPECTED_STATUS.format(
                        link=pep_url,
                        status=status_text,
                        expected_status=EXPECTED_STATUS[status_in_list]
                    ))
                    STATUS_COUNT[status.text] += 1
    filepath = BASE_DIR / 'results' / 'pep_parse_result.csv'
    with open(filepath, 'w') as csv_file:
        writer = csv.writer(csv_file, dialect='unix')
        writer.writerow(['Status', 'Count'])
        total = 0
        for status, count in STATUS_COUNT.items():
            writer.writerow([status, count])
            total += count
        writer.writerow(['Total', total])


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


# Код этой функции обновите.
def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    # Логируем переданные аргументы командной строки.
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()

    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    # Если из функции вернулись какие-то результаты,
    if results is not None:
        # передаём их в функцию вывода вместе с аргументами командной строки.
        control_output(results, args)

    # Логируем завершение работы парсера.
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
