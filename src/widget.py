from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str | None:
    """Функция mask_account_card принимает на вход строку формата
    Visa Platinum 7000792289606361, или Maestro 7000792289606361, или Счет 73654108430135874305.
    Для маскировки номера карты/счета используются ранее написанные функции из модуля masks
    :param account_card: Строка формата Visa Platinum 7000792289606361, или Maestro 7000792289606361, или Счет 73654108430135874305
    :return: Строка формата Visa Platinum 7000 79** **** 6361, или Maestro 7000 79** **** 6361, или Счет **4305
    """

    if not account_card or not isinstance(account_card, str):
        return None
    try:
        number = int(account_card.split()[-1])  # Преобразуем в целое число для проверки длины
        prefix = account_card[:-len(str(number))]  # Преобразуем в строку для проверки длины

        if len(str(number)) == 16:
            masked = get_mask_card_number(str(number))  # Преобразуем в строку для маскировки
            return f"{prefix}{masked}"
        elif len(str(number)) == 20:
            masked = get_mask_account(str(number))  # Преобразуем в строку для маскировки
            return f"{prefix}{masked}"
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
    try:
        # Пытаемся преобразовать строку в объект datetime
        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        # Возвращаем дату в нужном формате
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        # Если строка некорректна, возвращаем None
        return None
    new_date: list[str] = date[0:10].split("-")
    return ".".join(new_date[::-1])