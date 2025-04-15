"""Проект развивается, и источником данных о финансовых транзакциях теперь может быть не только JSON-файл,
но и CSV- или XLSX-файл. Благодаря знаниям о библиотеке pandas наконец можно реализовать поддержку новых
форматов данных.

Файлы
 Data/transactions.csv и
 Data/transactions_excel.xlsx
используйте для работы над задачами.

Задачи
 Реализовать считывание финансовых операций из CSV- и XLSX-файлов.
* Дополнительное задание
Типизируйте написанный код и добейтесь того, чтобы mypy при запуске не выдавал ошибок.
Напишите тесты для новых функций.
"""

from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, Dict, List, Union, cast

import pandas as pd


def read_csv_transactions(file_path: Union[str, Path, StringIO, BytesIO]) -> List[Dict[str, Any]]:
    """
    Чтение транзакций из CSV файла.

    Функция считывает данные из CSV файла, используя точку с запятой в качестве разделителя,
    и преобразует их в список словарей. Пропущенные значения (NaN) заменяются на None.

    Args:
        file_path: Путь к CSV файлу. Может быть строкой, объектом Path или файлоподобным объектом.

    Returns:
        List[Dict[str, Any]]: Список словарей, где каждый словарь представляет одну транзакцию.
            Ключи словаря - названия колонок, значения - соответствующие данные.
    """
    df = pd.read_csv(file_path, sep=';')
    transactions = df.replace({pd.NA: None}).to_dict('records')
    # Cast the keys to str since we know column names are strings
    return [cast(Dict[str, Any], {str(k): v for k, v in record.items()})
            for record in transactions]


def read_excel_transactions(file_path: Union[str, Path, BytesIO]) -> List[Dict[str, Any]]:
    """
    Чтение транзакций из Excel файла (XLSX).

    Функция считывает данные из Excel файла (поддерживаются форматы .xlsx и .xls)
    и преобразует их в список словарей. Пропущенные значения (NaN) заменяются на None.

    Args:
        file_path: Путь к Excel файлу. Может быть строкой, объектом Path или файлоподобным объектом.

    Returns:
        List[Dict[str, Any]]: Список словарей, где каждый словарь представляет одну транзакцию.
            Ключи словаря - названия колонок, значения - соответствующие данные.
    """
    df = pd.read_excel(file_path)
    transactions = df.replace({pd.NA: None}).to_dict('records')
    # Cast the keys to str since we know column names are strings
    return [cast(Dict[str, Any], {str(k): v for k, v in record.items()})
            for record in transactions]


def read_transactions(file_path: Union[str, Path, StringIO, BytesIO]) -> List[Dict[str, Any]]:
    """
    Чтение транзакций из файла с автоматическим определением формата.

    Функция определяет формат файла по расширению и вызывает соответствующую
    функцию для чтения данных. Поддерживаются форматы CSV, XLSX и XLS.
    Также принимает объекты StringIO/BytesIO для CSV/Excel соответственно.

    Args:
        file_path: Путь к файлу с транзакциями (str/Path) или файлоподобный объект (StringIO/BytesIO).

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями.

    Raises:
        ValueError: Если формат файла не поддерживается.
    """
    # Обработка файлоподобных объектов
    if isinstance(file_path, (StringIO, BytesIO)):
        if isinstance(file_path, StringIO):
            # StringIO только для CSV
            return read_csv_transactions(file_path)
        else:
            # BytesIO только для Excel
            return read_excel_transactions(file_path)

    path = Path(file_path) if isinstance(file_path, str) else file_path

    if path.suffix.lower() == '.csv':
        return read_csv_transactions(file_path)
    elif path.suffix.lower() in ('.xlsx', '.xls'):
        return read_excel_transactions(file_path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")
