import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (
    BASE_DIR, DATETIME_FORMAT, FILE_MODE,
    FILE_SAVE_MESSAGE, PRETTY_MODE, RESULTS_DIR
)


def default_output(results, *args):
    for row in results:
        print(*row)


def pretty_output(results, *args):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / RESULTS_DIR
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formated = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formated}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect=csv.unix_dialect)
        writer.writerows(results)
    logging.info(FILE_SAVE_MESSAGE.format(file_path=file_path))


OUTPUT_MODE = {
    PRETTY_MODE: pretty_output,
    FILE_MODE: file_output,
    None: default_output
}


def control_output(results, cli_args, outputs=OUTPUT_MODE):
    outputs[cli_args.output](results, cli_args)
