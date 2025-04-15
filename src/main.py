import json
import logging
from datetime import datetime
import os
import re
from sys import excepthook

import pandas as pd
from mypy.fastparse import parse_type_string
from pandas import describe_option
from pandas.core.dtypes.cast import infer_dtype_from
from pandas.core.methods.selectn import SelectNSeries
from pandas.io.common import file_path_to_url
from pandas.io.formats.format import return_docstring

from src.config import DATA_DIR
from src.config import LOG_DIR
from src.generators import card_number_generator

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


# Функция для чтения данных из файла
def load_transactions(file_path: str) -> list:
    if file_path.endswith(".csv"):
        try:
            # Указываем разделитель ";" при чтении CSV
            df = pd.read_csv(file_path, sep=';')
            transactions = []
            for _, row in df.iterrows():
                # Обратите внимание, что имена столбцов в CSV соответствуют заголовкам файла
                transaction = {
                    "id": str(row["id"]),
                    "state": row["state"],
                    "date": row["date"],
                    "operationAmount": {
                        "amount": row["amount"],
                        "currency": {
                            "name": row["currency_name"],  # В CSV это currency_name, не currency.name
                            "code": row["currency_code"]  # В CSV это currency_code, не currency.code
                        }
                    },
                    "from": row["from"] if pd.notna(row["from"]) else "",  # Обработка пустых значений
                    "to": row["to"],
                    "description": row["description"]
                }
                transactions.append(transaction)
            return transactions
        except Exception as e:
            logger.error(f"Ошибка при чтении файла csv {file_path}: {e}")
            raise
    elif file_path.endswith(".json"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                transactions = json.load(file)
                return transactions
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка при чтении файла json {file_path}: {e}")
            raise
    elif file_path.endswith(".xlsx"):
        try:
            df = pd.read_excel(file_path)
            transactions = []
            for _, row in df.iterrows():
                transaction = {
                    "id": str(row["id"]),
                    "state": row["state"],
                    "date": row["date"],
                    "operationAmount": {
                        "amount": row["amount"],
                        "currency": {
                            "name": row["currency_name"],
                            "code": row["currency_code"]
                        }
                    },
                    "from": row["from"] if pd.notna(row["from"]) else "",
                    "to": row["to"],
                    "description": row["description"]
                }
                transactions.append(transaction)
            return transactions
        except Exception as e:
            logger.error(f"Ошибка при чтении файла xlsx {file_path}: {e}")
            raise
    else:
        logger.error(f"Неподдерживаемый тип файла {file_path}")
        raise ValueError(f"Неподдерживаемый тип файла {file_path}")

# Функция форматирования вывода данных о транзакциях
def format_transaction(transaction):
    # Извлекаем дату и время из поля date
    datetime = transaction.get("date", "Не указано")
    description = transaction.get("description", "Не указано")

    # Извлекаем сумму и валюту из поля operationAmount
    amount = transaction.get("operationAmount", {}).get("amount", "Не указано")
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("name", "Не указано")

    # Извлекаем счет отправителя и получателя из полей from и to
    from_account = transaction.get("from", "Не указано")
    to_account = transaction.get("to", "Не указано")

    # Форматируем вывод данных о транзакции
    output = f"{datetime} {description}\n"
    output += f"{from_account} -> {to_account}\n"
    output += f"Сумма: {amount} {currency}\n"
    return output

def filter_transactions(transactions, search_string):
    """Фильтруем транзакции по строке поиска в описании"""
    # Пустая строка поиска - возвращаем все транзакции
    if not search_string:
        return transactions

    # Преобразуем строку поиска в нижний регистр
    search_pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    filtered = []

    for transaction in transactions:
        description = transaction["description"]
        print(f"Checking description: {description}") # Сообщение для отладки
        # Если строка поиска содержится в описании транзакции, добавляем ее в список отфильтрованных транзакций
        # Используем re.search() для поиска строки поиска в описании транзакции
        if search_pattern.search(description):
            filtered.append(transaction)

    return filtered

def mask_account(account_number: str) -> str:
    """Маскируем номер счета, показывая только последние 4 цифры"""
    parts = account_number.split()

    # Проверяем, что номер счета не пустой и состоит из цифр
    if len(parts) > 1 and parts[-1].isdigit():
        # Счет состоит из 6 цифр
        if len(parts[-1]) == 6:
            return f"{parts[0]} **{parts[-1][-3:]}" # Маскируем все кроме последних 3 цифр
        # Счет состоит из 4 цифр или больше
        elif len(parts[-1]) >= 4:
            return f"{parts[0]} **{parts[-1][-4:]}" # Маскируем все кроме последних 4 цифр

    return account_number # Если номер счета не соответствует формату, возвращаем его без изменений

def mask_card(card_info: str) -> str:
    """Маскируем номер карты, показывая только последние 4 цифры"""
    # Проверяем, что в строке есть название карты (Visa или Mastercard)
    if " " in card_info and not card_info.replace(" ", "").isdigit():
        # Разделяем строку на части по пробелу
        parts = card_info.rsplit(" ", 1) # Разделяем название карты по пробелу
        if len(parts) != 2:
            return card_info # Если не удалось разделить строку, возвращаем ее без изменений
        card_name = parts[0] # Название карты
        card_number = parts[1] # Номер карты
    else:
        card_name = "" # Если в строке нет названия карты, устанавливаем пустую строку
        card_number = card_info.strip() # Убираем лишние пробелы в начале и конце строки

    # Убираем пробелы из номера карты
    card_number_cleaned = card_number.replace(" ", "")

    # Проверяем, что номер карты состоит из 16 цифр
    if len(card_number_cleaned) < 12 and card_number_cleaned.isdigit():
        return card_info # Если номер карты не соответствует формату, возвращаем его без изменений

    # Маскируем номер карты, показывая только последние 4 цифры
    masked_card_number = f"{card_number_cleaned[:4]} {card_number_cleaned[4:6]}** {card_number_cleaned[-4:]}"

    # Возвращаем маскированный номер карты с названием карты
    if card_name:
        return f"{card_name} {masked_card_number}"
    else:
        return masked_card_number


def format_date(date_str):
    """Форматируем дату в формате ДД.ММ.ГГГГ"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        formatted_date = date.strftime("%d.%m.%Y")
        return formatted_date
    except ValueError:
        return date_str


def print_transaction(transaction):
    """Выводим информацию о транзакции"""
    date = format_date(transaction["date"])
    description = transaction["description"]

    # Маскируем номер карты или счета отправителя и получателя
    from_account = mask_account(transaction["from"])
    to_account = mask_account(transaction["to"])

    # Меняем NaN или пустую строку на пробел
    if isinstance(from_account, float) or not from_account:
        from_account = " " # Заменяем NaN или пустую строку на пробел
    if isinstance(to_account, float) or not to_account:
        to_account = " " # Заменяем NaN или пустую строку на пробел

    # Маскируем номер карты или счета отправителя и получателя
    if "карта" in description.lower(): #Если в описании есть слово "карта"
        from_account = mask_card(from_account) if from_account != " " else from_account
        to_account = mask_card(to_account) if to_account != " " else to_account
    else:
        from_account = mask_account(from_account) if "счет" in str(from_account).lower() else mask_card(from_account)
        to_account = mask_account(from_account) if "счет" in str(from_account).lower() else mask_card(from_account)

    #Форматируем вывод в зависимости от типа операции
    if "перевод" in description.lower():
        print(f"{date} {description}")
        print(f"{from_account} -> {to_account}")
    elif "открытие вклада" in description.lower():
        print(f"{date} {description}")
        print(f"{to_account}") # Выводим только to_account
    else:
        print(f"{date} {description}")
        print(f"{from_account}")

    # Проверяем, есть ли поле "operationAmount" в транзакции
    if "operationAmount" in transaction:
        amount = transaction["operationAmount"]["amount"]
        currency = transaction["operationAmount"]["currency"]["name"]
        print(f"Сумма: {amount} {currency}\n")
    else:
        print("Сумма: Неизвестна\n") # Информацию о сумме не удалось получить


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ")

    if choice == "1":
        file_path = os.path.join(DATA_DIR, "operations.json")
        transactions = load_transactions(file_path)
        print("Программа: Для обработки выбран JSON-файл.")
    elif choice == "2":
        file_path = os.path.join(DATA_DIR, "transactions.csv")
        transactions = load_transactions(file_path)
        print("Программа: Для обработки выбран CSV-файл.")
    elif choice == "3":
        file_path = os.path.join(DATA_DIR, "transactions_excel.xlsx")
        transactions = load_transactions(file_path)
        print("Программа: Для обработки выбран XLSX-файл.")
    else:
        print("Программа: Некорректный выбор. Пожалуйста, выберите пункт меню 1, 2 или 3.")
        return

    # Фильтруем и сортируем транзакции по статусу

    statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = (
            input(
                "Введите статус транзакции (EXECUTED, CANCELED или PENDING): "
                "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\nПользователь: "
            )
            .upper()
            .strip()
        )
        if status in statuses:
            print(f'Программа: Операции отфильтрованы по статусу "{status}"')
            filtered_transactions = [
                t for t in transactions if str(t.get("state", "")).upper() == status
            ] # Преобразование в строку
            break
        else:
            print(f'Программа: Статус операции "{status}" не найден. Пожалуйста, введите корректный статус.')

    # Дополнительные фильтры
    sort_choice = input("Отсортировать операции по дате? (Да/Нет): ").strip().lower()
    if sort_choice == "да":
        order_choice = input("По возрастанию или убыванию? (Возрастание/Убывание)\nПользователь: ").strip().lower()
        if order_choice == "по возрастанию":
            filtered_transactions.sort(key=lambda x: x["date"])
        elif order_choice == "по убыванию":
            filtered_transactions.sort(key=lambda x: x["date"], reverse=True)

    currency_choice = input("Выводить только рублевые транзакции? (Да/Нет)\nПользователь: ").strip().lower()
    if currency_choice == "да":
        filtered_transactions = [
            t
            for t in filtered_transactions
            if "operationAmount" in t and t["operationAmount"]["currency"]["code"] == "RUB"
        ]

    description_filter = (
        input("Отфильтровать список транзакций по определенному слову в описании? (Да/Нет)\nПользователь: ")
        .strip()
        .lower()
    )
    if description_filter == "да":
        search_string = input("Введите строку для поиска в описании: ")
        filtered_transactions = filter_transactions(filtered_transactions, search_string)

    # Выводим отфильтрованные транзакции
    print("Распечатываю итоговый список транзакций...:")
    if filtered_transactions:
        print(f"Всего банковских транзакций в выборке: {len(filtered_transactions)}")
        for transaction in filtered_transactions:
            print_transaction(transaction)
    else:
        print("Не найдено транзакций, соответствующих заданным критериям.")


if __name__ == "__main__":
    main()