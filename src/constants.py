from pathlib import Path
from urllib.parse import urljoin

HEADS_OF_LATEST_VERSIONS_TABLE = (
    'Ссылка на статью', 'Заголовок', 'Редактор, автор'
)
HEADS_OF_WHATS_NEW_TABLE = ('Ссылка на статью', 'Заголовок', 'Редактор, Автор')

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

PATTERN_FOR_PEP_PARSE = (
    r'(Rejected|Active|Accepted|Deferred|Final|'
    r'Provisional|Superseded|Withdrawn|Draft|April Fool!)$'
)
PATTERN_FOR_LATEST_VERSIONS = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

PRETTY_MODE = 'pretty'
FILE_MODE = 'file'

START_PARSER_MESSAGE = 'Парсер запущен!'
PARSER_ARGS_MESSAGE = 'Аргументы командной строки: {args}'
PARSER_FINISHED = 'Парсер завершил работу'
RESULT_DOWNLOAD_MESSAGE = 'Архив был загружен и сохранён: {archive_path}'
FILE_SAVE_MESSAGE = 'Файл с результатами был сохранён: {file_path}'
UNEXPECTED_STATUS = ('\nНесовпадающие статусы:\n{link}\nСтатус в карточке: '
                     '{status}\nОжидаемые статусы:\n{expected_status}')

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_URL = 'https://peps.python.org/'
WHATS_NEW_URL = urljoin(MAIN_DOC_URL, 'whatsnew/')
DOWNLOADS_URL = urljoin(MAIN_DOC_URL, 'download.html')

TAG_ERROR_MESSAGE = 'Не найден тег {tag} {attrs}'
ERROR_MESSAGE_URL = 'Не удалось получить информацию по странице {url}'
CONNECTION_ERROR_MESSAGE = 'Возникла ошибка при загрузке страницы {url}'
LATEST_VERSIONS_ERROR_MESSAGE = 'Не найден список c версиями Python'
PROGRAMM_ERROR_MESSAGE = 'Сбой в работе программы: {error}'

BASE_DIR = Path(__file__).parent
DOWNLOAD_DIR = 'downloads'
RESULTS_DIR = 'results'
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
