import json
import logging
import os
import re
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

from src.config import DATA_DIR, LOG_DIR


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(LOG_DIR, "app.log"), encoding="utf-8")
    ],
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


# Функция для чтения данных из файла
def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    if file_path.endswith(".csv"):
        try:
            df = pd.read_csv(file_path, sep=';')
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


def format_transaction(transaction: Dict[str, Any]) -> str:
    datetime_str = transaction.get("date", "Не указано")
    description = transaction.get("description", "Не указано")
    amount = transaction.get("operationAmount", {}).get("amount", "Не указано")
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("name", "Не указано")
    from_account = transaction.get("from", "Не указано")
    to_account = transaction.get("to", "Не указано")

    output = f"{datetime_str} {description}\n"
    output += f"{from_account} -> {to_account}\n"
    output += f"Сумма: {amount} {currency}\n"
    return output


def filter_transactions(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    if not search_string:
        return transactions

    search_pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    filtered = []

    for transaction in transactions:
        description = transaction["description"]
        if search_pattern.search(description):
            filtered.append(transaction)

    return filtered


def mask_account(account_number: str) -> str:
    parts = account_number.split()
    if len(parts) > 1 and parts[-1].isdigit():
        if len(parts[-1]) == 6:
            return f"{parts[0]} **{parts[-1][-3:]}"
        elif len(parts[-1]) >= 4:
            return f"{parts[0]} **{parts[-1][-4:]}"
    return account_number


def mask_card(card_info: str) -> str:
    if " " in card_info and not card_info.replace(" ", "").isdigit():
        parts = card_info.rsplit(" ", 1)
        if len(parts) != 2:
            return card_info
        card_name, card_number = parts
    else:
        card_name = ""
        card_number = card_info.strip()

    card_number_cleaned = card_number.replace(" ", "")
    if len(card_number_cleaned) < 12 and card_number_cleaned.isdigit():
        return card_info

    masked_card_number = f"{card_number_cleaned[:4]} {card_number_cleaned[4:6]}** {card_number_cleaned[-4:]}"
    return f"{card_name} {masked_card_number}" if card_name else masked_card_number


def format_date(date_str: str) -> str:
    try:
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        return date.strftime("%d.%m.%Y")
    except ValueError:
        return date_str


def print_transaction(transaction: Dict[str, Any]) -> None:
    date = format_date(transaction["date"])
    description = transaction["description"]

    # Обработка поля 'from' с проверкой на наличие
    from_account = mask_account(transaction.get("from", "")) if isinstance(transaction.get("from"), str) else " "
    # Обработка поля 'to' с проверкой на наличие
    to_account = mask_account(transaction.get("to", "")) if isinstance(transaction.get("to"), str) else " "

    if "карта" in description.lower():
        from_account = mask_card(from_account) if from_account != " " else from_account
        to_account = mask_card(to_account) if to_account != " " else to_account
    else:
        from_account = mask_account(from_account) if "счет" in str(from_account).lower() else mask_card(from_account)
        to_account = mask_account(to_account) if "счет" in str(to_account).lower() else mask_card(to_account)

    if "перевод" in description.lower():
        print(f"{date} {description}")
        print(f"{from_account} -> {to_account}")
    elif "открытие вклада" in description.lower():
        print(f"{date} {description}")
        print(f"{to_account}")
    else:
        print(f"{date} {description}")
        print(f"{from_account}")

    if "operationAmount" in transaction:
        amount = transaction["operationAmount"]["amount"]
        currency = transaction["operationAmount"]["currency"]["name"]
        print(f"Сумма: {amount} {currency}\n")
    else:
        print("Сумма: Неизвестна\n")


def main() -> None:
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

    statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input(
            "Введите статус транзакции (EXECUTED, CANCELED или PENDING): "
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\nПользователь: "
        ).upper().strip()
        if status in statuses:
            print(f'Программа: Операции отфильтрованы по статусу "{status}"')
            filtered_transactions = [
                t for t in transactions if str(t.get("state", "")).upper() == status
            ]
            break
        else:
            print(f'Программа: Статус операции "{status}" не найден. Пожалуйста, введите корректный статус.')

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

    description_filter = input(
        "Отфильтровать список транзакций по определенному слову в описании? (Да/Нет)\nПользователь: "
    ).strip().lower()
    if description_filter == "да":
        search_string = input("Введите строку для поиска в описании: ")
        filtered_transactions = filter_transactions(filtered_transactions, search_string)

    print("Распечатываю итоговый список транзакций...:")
    if filtered_transactions:
        print(f"Всего банковских транзакций в выборке: {len(filtered_transactions)}")
        for transaction in filtered_transactions:
            print_transaction(transaction)
    else:
        print("Не найдено транзакций, соответствующих заданным критериям.")


if __name__ == "__main__":
    main()
