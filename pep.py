import csv

from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
BASE_DIR = Path(__file__).parent

data = [['hostname', 'vendor', 'model', 'location'],
        ['sw1', 'Cisco', '3750', 'London, Best str'],
        ['sw2', 'Cisco', '3850', 'Liverpool, Better str'],
        ['sw3', 'Cisco', '3650', 'Liverpool, Better str'],
        ['sw4', 'Cisco', '3650', 'London, Best str']]


STATUS_COUNT = {
    'Active': 0,
    'Accepted': 0,
    'Deferred': 0,
    'Final': 0,
    'Provisional': 0,
    'Rejected': 0,
    'Superseded': 0,
    'Withdrawn': 0,
    'Draft': 0
}

csv_dir = BASE_DIR
filename = 'csv_result'
path = csv_dir / filename
# with open(path, 'w', encoding='utf-8') as csv_file:
#     writer = csv.writer(csv_file, dialect='unix')
#     heads_table = ['Status', 'Count']
#     writer.writerow(heads_table)
#     for status in STATUS_COUNT.keys():
#         writer.writerows(status
STATUS_COUNT = {
    'Active': 37,
     'Accepted': 40,
     'Deferred': 36,
     'Final': 264,
     'Provisional': 0,
     'Rejected': 120,
     'Superseded': 19,
     'Withdrawn': 55,
     'Draft': 30
}

with open('pep_parse_result.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, dialect='unix')
    writer.writerow(['Status', 'Count'])
    total = 0
    for status, count in STATUS_COUNT.items():
        writer.writerow([status, count])
        total += count
    writer.writerow(['Total', total])