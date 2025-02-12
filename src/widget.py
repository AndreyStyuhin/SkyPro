from masks import get_mask_account, get_mask_card_number


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
    """Функция get_date, которая принимает на вход строку с датой в формате
    "2024-03-11T02:26:18.671407" и возвращает строку с датой в формате
    "ДД.ММ.ГГГГ" ("11.03.2024")'"""
    new_date = date[0:10].split("-")
    return ".".join(new_date[::-1])

