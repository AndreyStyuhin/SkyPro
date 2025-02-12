from email.utils import parsedate_to_datetime

from masks import get_mask_card_number, get_mask_account
from datetime import datetime

def mask_account_card (account_card: str) -> str | None:
    """Функция mask_account_card принимает на вход строку формата
Visa Platinum 7000792289606361, или Maestro 7000792289606361, или Счет 73654108430135874305.
Для маскировки номера карты/счета используются ранее написанные функции из модуля masks
"""
    if "Счет" in account_card:
        masked_account = get_mask_account(int(account_card.split()[-1]))
        return f"Счет **{masked_account[-4:]}"
    else:
        masked_card = get_mask_card_number(int(account_card.split()[-1]))
        return f"{account_card.split()[0]} {masked_card}"


def get_date(date: str) -> str | None:
    """Функция get_date принимает на вход строку и отдает корректный результат
    в формате 11.07.2018."""
    date_parts = date.split()
    raw_date = datetime.strptime(date_parts[0], "%Y-%m-%d")
    return raw_date.strftime("%d.%m.%Y")



