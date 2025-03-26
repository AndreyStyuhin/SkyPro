"""Проект развивается, и источником данных о финансовых транзакциях теперь может быть не только JSON-файл,
но и CSV- или XLSX-файл. Благодаря знаниям о библиотеке pandas наконец можно реализовать поддержку новых форматов данных.

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

import pandas as pd
from typing import List, Dict, Any, Union
from pathlib import Path


def read_csv_transactions(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Чтение транзакций из CSV файла

    Args:
        file_path: Путь к CSV файлу

    Returns:
        Список словарей с транзакциями
    """
    df = pd.read_csv(file_path, sep=';')
    # Заменяем NaN на None для корректной работы с JSON
    transactions = df.replace({pd.NA: None}).to_dict('records')
    return transactions


def read_excel_transactions(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Чтение транзакций из Excel файла (XLSX)

    Args:
        file_path: Путь к XLSX файлу

    Returns:
        Список словарей с транзакциями
    """
    df = pd.read_excel(file_path)
    # Заменяем NaN на None для корректной работы с JSON
    transactions = df.replace({pd.NA: None}).to_dict('records')
    return transactions


def read_transactions(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Чтение транзакций из файла (автоматически определяет формат)

    Args:
        file_path: Путь к файлу

    Returns:
        Список словарей с транзакциями

    Raises:
        ValueError: Если формат файла не поддерживается
    """
    path = Path(file_path)
    if path.suffix.lower() == '.csv':
        return read_csv_transactions(path)
    elif path.suffix.lower() in ('.xlsx', '.xls'):
        return read_excel_transactions(path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")