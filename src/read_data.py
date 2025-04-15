import logging
import os
import re
from typing import Dict, List

from mypy.typeops import false_only
from requests.utils import dict_from_cookiejar

from src.config import DATA_DIR
from src.config import LOG_DIR
import pandas as pd

# Путь к директории с данными
csv_file_path = DATA_DIR / 'transactions.csv' # Путь к файлу CSV
excel_file_path = DATA_DIR / 'transactions.xlsx' # Путь к файлу Excel

# Создаем директорию для логов, если ее нет
logs_dir = DATA_DIR.parent / 'logs'
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Настраиваем логирование
log_file_path = logs_dir / 'transactions.log'
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

def read_transactions_from_csv(file_path: str) -> List[Dict[str, str]]:
    """Функция read_csv принимает на вход путь к файлу CSV и возвращает список словарей,
    где каждый словарь соответствует строке CSV файла.
    :param file_path: Путь к файлу CSV
    :return: Список словарей, где каждый словарь соответствует строке CSV файла
    """
    if not os.path.exists(file_path):
        logger.error(f"Файл {file_path} не найден")
        raise FileNotFoundError(f"Файл {file_path} не найден")
    try:
        df = pd.read_csv(file_path, sep=',', encoding='utf-8')
        transactions = df.to_dict(orient='records')
        return transactions
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        raise

def read_transactions_from_excel(file_path: str) -> List[Dict[str, str]]:
    """Функция read_excel принимает на вход путь к файлу Excel и возвращает список словарей,
    где каждый словарь соответствует строке Excel файла.
    :param file_path: Путь к файлу Excel
    :return: Список словарей, где каждый словарь соответствует строке Excel файла
    """
    if not os.path.exists(file_path):
        logger.error(f"Файл {file_path} не найден")
        raise FileNotFoundError(f"Файл {file_path} не найден")
    try:
        df = pd.read_excel(file_path)
        transactions = df.to_dict(orient='records')
        logger.info(f"Из файла {file_path} успешно прочитано {len(transactions)} записей")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        raise

def filter_transactions(transactions: List[Dict], search_string: str) -> List[Dict]:
    """Функция filter_transactions принимает на вход список словарей,
    где каждый словарь соответствует строке CSV файла, и строку filter_by,
    которая может принимать значения 'from', 'to', 'date', 'operationAmount' или 'state'.
    Функция возвращает список словарей, где каждый словарь соответствует строке CSV файла,
    отфильтрованный по значению filter_by.
    :param transactions: Список словарей, где каждый словарь соответствует строке CSV файла
    :param filter_by: Строка, которая может принимать значения 'from', 'to', 'date', 'operationAmount' или 'state'
    :return: Список словарей, где каждый словарь соответствует строке CSV файла, отфильтрованный по значению filter_by
    """
    logger.info(f"Фильтрация транзакций по {search_string}")
    pattern = re.compile(re.escape(search_string), re.IGNORECASE) # Создаем шаблон для поиска
    filtered_transactions = [
        transaction for transaction in transactions if pattern.search(transaction.get("description", ""))
    ]
    logger.info(f"Найдено {len(filtered_transactions)} транзакций")
    return filtered_transactions

def count_transactions_by_category(transactions: List[Dict], categories: List[str]) -> Dict[str, int]:
    """Функция count_transactions_by_category принимает на вход список словарей,
    где каждый словарь соответствует строке CSV файла, и список категорий,
    и возвращает словарь, где каждый ключ - это категория, а значение - количество транзакций в этой категории.
    :param transactions: Список словарей, где каждый словарь соответствует строке CSV файла
    :param categories: Список категорий
    :return: Словарь, где каждый ключ - это категория, а значение - количество транзакций в этой категории
    """
    logger.info("Подсчет транзакций по категориям")
    category_count = {category: 0 for category in categories}
    for transaction in transactions:
        description = transaction.get("description", "").lower()
        for category in categories:
            if category.lower() in description:
                category_count[category] += 1
    logger.info(f"Подсчитано {category_count} транзакций")
    return category_count