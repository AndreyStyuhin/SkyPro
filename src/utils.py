"""
Напишите функцию, которая принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.
Если файл пустой, содержит не список или не найден, функция возвращает пустой список. Функцию поместите в модуль utils.
Файл с данными о финансовых транзакциях operations.json поместите в директорию data/ в корне проекта.
def load_operations(path):
        Аргументы:
            path (str): Path to the JSON file

        Возвращает:
            list: List of dictionaries containing financial transaction data,
                 or empty list if file is not found, empty, or doesn't contain a list
"""

import json
import logging
from typing import List, Dict, Any
from src.external_api import convert_to_rub

def load_operations(path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.

    Аргументы:
        path (str): Путь к JSON-файлу.

    Возвращает:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях,
                              или пустой список, если файл не найден, пуст или не содержит список.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            logging.debug(f"Загружаем операции из {path}")
            data = json.load(file)
            if not data or not isinstance(data, list):
                logging.warning(f"Файл {path} не содержит корректный список операций")
                return []
            logging.info(f"Загрузка операций {len(data)} прошла успешно")
            return data
    except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
        logging.error(f"Ошибка при загрузке файла {path}: {e}")
        return []


"""Реализуйте функцию, которая принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях,
тип данных — float. 
Если транзакция была в USD или EUR, происходит обращение к внешнему API для получения текущего курса валют 
и конвертации суммы операции в рубли. Для конвертации валюты воспользуйтесь Exchange Rates Data API: 
https://apilayer.com/exchangerates_data-api. Функцию конвертации поместите в модуль external_api.
Используйте переменные окружения из файла .env для сокрытия чувствительных данных (токенов доступа для API).
Создайте шаблон файла .env и разместите в репозитории на GitHub.
Напишите тесты для новых функций, используйте Mock и patch."""


def load_transactions(data: List[Dict[str, Any]]) -> float:
    """
    Возвращает сумму всех транзакций в рублях.

    Аргументы:
        data (List[Dict[str, Any]]): Список транзакций.

    Возвращает:
        float: Сумма всех транзакций в рублях.
    """
    total_amount = 0.0
    for transaction in data:
        amount = transaction.get('amount', 0)
        currency = transaction.get('currency', 'RUB')
        try:
            total_amount += convert_to_rub(amount, currency)
        except ValueError as e:
            logging.error(f"Ошибка конвертации валюты: {e}")
    return total_amount