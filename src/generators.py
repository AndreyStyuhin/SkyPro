def filter_by_currency(transactions, currency):
    """Генератор, который фильтрует транзакции по заданной валюте."""
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction


def transaction_descriptions(transactions):
    """Генератор, который возвращает описание каждой транзакции по очереди."""
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start, end):
    """Генератор, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX."""
    for number in range(start, end + 1):
        # Форматируем номер с ведущими нулями, если это необходимо
        card_number = f"{number:016d}"
        # Форматируем номер с пробелами
        formatted_number = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
        yield formatted_number

# generators.py