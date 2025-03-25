"""
Напишите функцию, которая принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.
Если файл пустой, содержит не список или не найден, функция возвращает пустой список. Функцию поместите в модуль utils.
Файл с данными о финансовых транзакциях operations.json поместите в директорию data/ в корне проекта.
def load_operations(path):

"""

from typing import Union
import json
import requests
import logging
from typing import List, Dict, Any
import os
from dotenv import load_dotenv


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
            if not isinstance(data, list):  # Проверяем, что данные — это список
                logging.warning(f"Файл {path} не содержит корректный список операций")
                return []
            logging.info(f"Загрузка операций {len(data)} прошла успешно")
            return data  # Возвращаем список словарей
    except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
        logging.error(f"Ошибка при загрузке файла {path}: {e}")
        return []  # Возвращаем пустой список

"""Реализуйте функцию, которая принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях,
тип данных — float. 
Если транзакция была в USD или EUR, происходит обращение к внешнему API для получения текущего курса валют 
и конвертации суммы операции в рубли. Для конвертации валюты воспользуйтесь Exchange Rates Data API: 
https://apilayer.com/exchangerates_data-api. Функцию конвертации поместите в модуль external_api.
Используйте переменные окружения из файла .env для сокрытия чувствительных данных (токенов доступа для API).
Создайте шаблон файла .env и разместите в репозитории на GitHub.
Напишите тесты для новых функций, используйте Mock и patch."""


load_dotenv()  # Загружаем переменные окружения из .env

def convert_to_rub(amount: Union[int, float], currency: str) -> float:
    """
    Конвертирует сумму в рублях.

    Аргументы:
        amount (Union[int, float]): Сумма в исходной валюте.
        currency (str): Код валюты (например, "USD", "EUR").

    Возвращает:
        float: Сумма в рублях.
    """
    if currency == "RUB":
        return float(amount)  # Убедимся, что возвращаем float


    # Получаем API ключ из переменных окружения
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        raise ValueError("API ключ для конвертации валюты не найден")

    # Запрос к API для получения курса валют
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise ValueError(f"Ошибка при запросе к API: {response.status_code}")

    data = response.json()
    if "result" not in data:
        raise ValueError("Невозможно получить курс валюты")

    return float(data["result"])  # Убедимся, что возвращаем float