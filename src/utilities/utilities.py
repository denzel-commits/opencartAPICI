import csv
import os


def csv_reader(filename: str) -> list[dict]:
    if not os.path.exists(filename):
        raise FileNotFoundError(
            f'Файл {filename} не найден,\n'
            'пожалуйста, предоставьте файл по указанному пути')

    with open(filename, "r", newline="") as csvfile:
        return list(csv.DictReader(csvfile))
