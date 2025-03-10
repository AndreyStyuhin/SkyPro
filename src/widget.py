def mask_account_card(account_card: str) -> str | None:
    """Функция mask_account_card принимает на вход строку формата
    Visa Platinum 7000792289606361, или Maestro 7000792289606361, или Счет 73654108430135874305.
    Для маскировки номера карты/счета используются ранее написанные функции из модуля masks
    :param account_card: Строка формата Visa Platinum 7000792289606361, или Maestro 7000792289606361,
    или Счет 73654108430135874305
    :return: Строка формата Visa Platinum 7000 79** **** 6361, или Maestro 7000 79** **** 6361, или Счет **4305
    """

    if not account_card or not isinstance(account_card, str):
        return None

    try:
        parts = account_card.split()
        number = parts[-1]
        prefix = " ".join(parts[:-1])

        if len(number) == 16:
            masked = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
            return f"{prefix} {masked}"
        elif len(number) == 20:
            masked = f"**{number[-4:]}"
            return f"{prefix} {masked}"
        return None
    except Exception:
        return None


def get_date(date: str) -> str | None:
    """Функция get_date, которая принимает на вход строку с датой в формате
    "2024-03-11T02:26:18.671407" и возвращает строку с датой в формате
    "ДД.ММ.ГГГГ" ("11.03.2024")'
    :param date: Строка с датой в формате "2024-03-11T02:26:18.671407"
    :return: Строка с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024")
    """
    if (
        not date
        or not isinstance(date, str)
        or len(date) < 10
        or date[4] != "-"
        or date[7] != "-"
        or "T" not in date
    ):
        return None

    try:
        new_date: list[str] = date[0:10].split("-")
        return ".".join(new_date[::-1])
    except Exception:
        return None
