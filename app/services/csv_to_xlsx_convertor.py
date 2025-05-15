"""Домашнє завдання 11

11.1 Зробити конвертор для csv у xlsx та навпаки.
"""

import re

import pandas as pd
from pandas._typing import FilePath


def convert_csv_xlsx(filename: FilePath) -> None:
    """The function converts a csv file into an xlsx file or vice versa.

    Args:
        filename (FilePath): str, path object, file-like object
    """
    _csv_filetype = r"(\.csv$|\.CSV$)"
    _xlsx_filetype = r"(\.xlsx$|\.XLSX$)"

    if re.findall(_csv_filetype, filename):
        file_xlsx = re.sub(_csv_filetype, ".xlsx", filename)
        pd.read_csv(filename).to_excel(file_xlsx, index=False)
        return file_xlsx

    elif re.findall(_xlsx_filetype, filename):
        file_csv = re.sub(_xlsx_filetype, ".csv", filename)
        pd.read_excel(filename).to_csv(file_csv, index=False)
        return file_csv

    else:
        raise ValueError("This file type is not supported.\n")
