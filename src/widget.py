
from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str | None:
    if not account_card or not isinstance(account_card, str):
        return None
    """Функция mask_account_card принимает на вход строку формата
    Visa Platinum 7000792289606361, или Maestro 7000792289606361, или Счет 73654108430135874305.
    Для маскировки номера карты/счета используются ранее написанные функции из модуля masks
    """
    try:
        number = account_card.split()[-1]
        prefix = account_card[:-len(number)]

        if len(number) == 16:
            masked = get_mask_card_number(number)
            return f"{prefix}{masked}"
        elif len(number) == 20:
            masked = get_mask_account(number)
            return f"{prefix}{masked}"
        return None
    except Exception:
        return None


def get_date(date: str) -> str | None:
    """Функция get_date, которая принимает на вход строку с датой в формате
    "2024-03-11T02:26:18.671407" и возвращает строку с датой в формате
    "ДД.ММ.ГГГГ" ("11.03.2024")'"""
    new_date: list[str] = date[0:10].split("-")
    return ".".join(new_date[::-1])
