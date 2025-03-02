def get_mask_card_number(card_number: int) -> str:
    """Возвращает маскированный номер карты в формате: XXXX XX** **** XXXX. Отображаются первые 6 цифр (4+2),
    следующие 2 цифры заменяются на "**", за ними следуют ещё 4 скрытые цифры "****",
    и последние 4 цифры номера отображаются без маски.
    :param card_number: Номер банковской карты в виде целого числа.
    :return: Маскированный номер карты в виде строки."""

    card_str = str(card_number)
    if len(card_str) != 16:
        raise ValueError("Номер карты должен содержать ровно 16 цифр.")
    # Пример:
    # Вход: 7000792289606361
    # Результат: "7000 79** **** 6361"
    masked_card = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"

    return masked_card


print(get_mask_card_number(7000792289606361))


def get_mask_account(account_number: int) -> str:
    """Возвращает маскированный номер счета в формате: **XXXX.
    Отображаются последние 4 цифры, а первые 2 цифры заменяются на "**".
    :param account_number: Номер счета в виде целого числа.
    :return: Маскированный номер счета в виде строки."""

    account_str = str(account_number)
    if len(account_str) != 20:
        raise ValueError("Номер счета должен содержать ровно 20 цифр.")

    # Маскируем первые 2 цифры и оставляем последние 4 цифры
    masked_account = f"**{account_str[-4:]}"

    return masked_account


print(get_mask_account(11234567890123456789))
