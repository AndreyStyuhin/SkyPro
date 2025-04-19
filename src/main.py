"""
Программа: Привет! Добро пожаловать в программу работы
с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла

Пользователь: 1

Программа: Для обработки выбран JSON-файл.

После пользователь выбирает статус интересующих его операций.
Не забудьте, что для пользователя
executed
,
Executed
 и
EXECUTED
 — это одно и то же, а для программы — разное. Используйте приведение к единому регистру.

Программа: Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING

Пользователь: EXECUTED

Программа: Операции отфильтрованы по статусу "EXECUTED"

В случае, если пользователь ввел неверный статус, программа не должна падать в ошибку, а должна возвращать
пользователя к вводу корректного статуса:

Пользователь: test

Программа: Статус операции "test" недоступен.

Программа: Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING

После фильтрации программа выводит следующие вопросы для уточнения выборки операций, необходимых пользователю,
и выводит в консоль операции, соответствующие выборке пользователя:
Программа: Отсортировать операции по дате? Да/Нет

Пользователь: да

Программа: Отсортировать по возрастанию или по убыванию?

Пользователь: по возрастанию/по убыванию

Программа: Выводить только рублевые тразакции? Да/Нет

Пользователь: да

Программа: Отфильтровать список транзакций по определенному слову
в описании? Да/Нет

Пользователь: да/нет

Программа: Распечатываю итоговый список транзакций...

Программа:
Всего банковских операций в выборке: 4

08.12.2019 Открытие вклада
Счет **4321
Сумма: 40542 руб.

12.11.2019 Перевод с карты на карту
MasterCard 7771 27** **** 3727 -> Visa Platinum 1293 38** **** 9203
Сумма: 130 USD

18.07.2018 Перевод организации
Visa Platinum 7492 65** **** 7202 -> Счет **0034
Сумма: 8390 руб.

03.06.2018 Перевод со счета на счет
Счет **2935 -> Счет **4321
Сумма: 8200 EUR

Если выборка оказалась пустой, программа выводит сообщение:

Программа: Не найдено ни одной транзакции, подходящей под ваши
условия фильтрации

Задача main.py - объединить весь ранее описанный функционал. Для этого нужно использовать ранее описанные функции.
Реализовать импорт функции открытия файла JSON - из utils.load_operations
Реализовать импорт функции открытия файлов CSV и XLSX - из utils_csv.read_csv_transactions и
utils_csv.read_excel_transactions
Реализовать импорт функции фильтрации по статусу - из processing.filter_by_state
Реализовать импорт функции сортировки по дате - processing.sort_by_date
Реализовать импорт функции фильтрации по валюте - из generators.filter_by_currency
Реализовать импорт функции форматирования даты - widget.get_date
Реализовать импорт функции маскировки счёта и карты - widget.mask_account_card
Реализовать функцию поиска операций по заданной строке
Реализовать функцию подсчёта операций по категориям
"""

import logging
import os
import re
from collections import Counter
from typing import Dict, List, Any

# Импортируем необходимые функции из других модулей
from src.utils import load_operations
from src.utils_csv import read_csv_transactions, read_excel_transactions
from src.processing import filter_by_state, sort_by_date
from src.generators import filter_by_currency
from src.widget import get_date, mask_account_card
from src.config import DATA_DIR, LOG_DIR

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(LOG_DIR, "app.log"),
        encoding="utf-8")],
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из файла в зависимости от его формата

    Args:
        file_path: Путь к файлу с транзакциями

    Returns:
        Список транзакций

    Raises:
        ValueError: Если формат файла не поддерживается
        Exception: При ошибке чтения файла
    """
    if file_path.endswith(".csv"):
        try:
            return read_csv_transactions(file_path)
        except Exception as e:
            logger.error(f"Ошибка при чтении файла csv {file_path}: {e}")
            raise
    elif file_path.endswith(".json"):
        try:
            return load_operations(file_path)
        except Exception as e:
            logger.error(f"Ошибка при чтении файла json {file_path}: {e}")
            raise
    elif file_path.endswith(".xlsx"):
        try:
            return read_excel_transactions(file_path)
        except Exception as e:
            logger.error(f"Ошибка при чтении файла xlsx {file_path}: {e}")
            raise
    else:
        logger.error(f"Неподдерживаемый тип файла {file_path}")
        raise ValueError(f"Неподдерживаемый тип файла {file_path}")


def filter_transactions_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по строке поиска в описании

    Args:
        transactions: Список транзакций
        search_string: Строка для поиска в описании

    Returns:
        Отфильтрованный список транзакций
    """
    if not search_string:
        return transactions

    search_pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    filtered = []

    for transaction in transactions:
        description = transaction.get("description", "")
        if search_pattern.search(description):
            filtered.append(transaction)

    return filtered


def count_transactions_by_category(transactions: List[Dict[str, Any]]) -> Counter:
    """Подсчитывает количество операций по категориям

    Args:
        transactions: Список транзакций

    Returns:
        Counter с количеством операций по категориям
    """
    categories: Counter[str] = Counter()

    for transaction in transactions:
        description = transaction.get("description", "Неизвестно")
        # Определяем категорию по ключевым словам в описании
        if "перевод" in description.lower():
            categories["Переводы"] += 1
        elif "открытие вклада" in description.lower():
            categories["Вклады"] += 1
        elif "оплата" in description.lower():
            categories["Платежи"] += 1
        else:
            categories["Прочее"] += 1

    return categories


def print_transaction(transaction: Dict[str, Any]) -> None:
    """Выводит информацию о транзакции

    Args:
        transaction: Словарь с данными транзакции
    """
    date = get_date(transaction["date"])
    description = transaction["description"]

    # Получаем маскированные номера счетов/карт
    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")

    # Маскируем номера счетов и карт
    if from_account:
        from_account = mask_account_card(from_account)
    if to_account:
        to_account = mask_account_card(to_account)

    # Форматируем вывод в зависимости от типа операции
    if from_account and to_account:
        print(f"{date} {description}")
        print(f"{from_account} -> {to_account}")
    elif to_account:
        print(f"{date} {description}")
        print(f"{to_account}")
    elif from_account:
        print(f"{date} {description}")
        print(f"{from_account}")
    else:
        print(f"{date} {description}")

    # Выводим информацию о сумме
    if "operationAmount" in transaction:
        amount = transaction["operationAmount"]["amount"]
        currency = transaction["operationAmount"]["currency"]["name"]
        print(f"Сумма: {amount} {currency}\n")
    else:
        print("Сумма: Неизвестна\n")


def main() -> None:
    """Основная функция программы"""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ")

    if choice == "1":
        file_path = os.path.join(DATA_DIR, "operations.json")
        print("Программа: Для обработки выбран JSON-файл.")
    elif choice == "2":
        file_path = os.path.join(DATA_DIR, "transactions.csv")
        print("Программа: Для обработки выбран CSV-файл.")
    elif choice == "3":
        file_path = os.path.join(DATA_DIR, "transactions_excel.xlsx")
        print("Программа: Для обработки выбран XLSX-файл.")
    else:
        print("Программа: Некорректный выбор. Пожалуйста, выберите пункт меню 1, 2 или 3.")
        return

    try:
        transactions = load_transactions(file_path)
    except Exception as e:
        logger.error(f"Ошибка при загрузке транзакций: {e}")
        print(f"Программа: Произошла ошибка при загрузке файла: {e}")
        return

    # Фильтруем транзакции по статусу
    statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input("Пользователь: ").upper().strip()

        if status in statuses:
            print(f'Программа: Операции отфильтрованы по статусу "{status}"')
            filtered_transactions = filter_by_state(transactions, status)
            break
        else:
            print(f'Программа: Статус операции "{status}" недоступен.')

    # Сортировка по дате
    print("Программа: Отсортировать операции по дате? Да/Нет")
    sort_choice = input("Пользователь: ").strip().lower()
    if sort_choice == "да":
        print("Программа: Отсортировать по возрастанию или по убыванию?")
        order_choice = input("Пользователь: ").strip().lower()
        reverse = "убыван" in order_choice
        filtered_transactions = sort_by_date(filtered_transactions, reverse)

    # Фильтрация по валюте
    print("Программа: Выводить только рублевые тразакции? Да/Нет")
    currency_choice = input("Пользователь: ").strip().lower()
    if currency_choice == "да":
        filtered_transactions = list(filter_by_currency(filtered_transactions, "RUB"))

    # Фильтрация по описанию
    print("Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    description_filter = input("Пользователь: ").strip().lower()
    if description_filter == "да":
        search_string = input("Программа: Введите слово для поиска: ")
        filtered_transactions = filter_transactions_by_description(filtered_transactions, search_string)

    # Выводим отфильтрованные транзакции
    print("Программа: Распечатываю итоговый список транзакций...")

    if filtered_transactions:
        print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
        for transaction in filtered_transactions:
            print_transaction(transaction)
    else:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")


if __name__ == "__main__":
    main()
