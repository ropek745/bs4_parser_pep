from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
BASE_DIR = Path(__file__).parent
PEP_URL = 'https://peps.python.org/'
PATTERN = (r'(Rejected|Active|Accepted|Deferred|Final|'
           r'Provisional|Superseded|Withdrawn|Draft|April Fool!)$')

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
STATUS_COUNT = {
    'Active': 0,
    'Accepted': 0,
    'Deferred': 0,
    'Final': 0,
    'Provisional': 0,
    'Rejected': 0,
    'Superseded': 0,
    'Withdrawn': 0,
    'Draft': 0,
    'April Fool!': 0
}
UNEXPECTED_STATUS = ('\nНесовпадающие статусы:\n{link}\nСтатус в карточке: '
                     '{status}\nОжидаемые статусы:\n{expected_status}')
