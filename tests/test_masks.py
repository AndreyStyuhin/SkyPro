import pytest

from src.masks import get_mask_card_number
from src.masks import get_mask_account


@pytest.mark.parametrize(
    "input_card, expected",
    [
        (7000792289606361, "7000 79** **** 6361"),  # Корректный номер карты
        (1234567890123456, "1234 56** **** 3456"),  # Корректный номер карты
        (9876543210987654, "9876 54** **** 7654"),  # Корректный номер карты
        (123456789012345, "1234 56** **** 345"),  # Некорректный номер карты (меньше 16 цифр)
        (12345678901234567, "1234 56** **** 34567"),  # Некорректный номер карты (больше 16 цифр)
    ]
)
def test_get_mask_card_number():
    # Тест с корректным номером карты
    input_card = 7000792289606361
    expected = "7000 79** **** 6361"
    assert get_mask_card_number(input_card) == expected

    # Тест с некорректным номером карты (меньше 16 цифр)
    try:
        get_mask_card_number(123456789012345)  # 15 цифр
    except ValueError as e:
        assert str(e) == "Номер карты должен содержать ровно 16 цифр."

    # Тест с некорректным номером карты (больше 16 цифр)
    try:
        get_mask_card_number(12345678901234567)  # 17 цифр
    except ValueError as e:
        assert str(e) == "Номер карты должен содержать ровно 16 цифр."


# Запуск теста
test_get_mask_card_number()
# tests/test_masks.py


@pytest.mark.parametrize(
    "input_account, expected",
    [
        (12345678901234567890, "**7890"),  # номер счета из 20 цифр
    ]
)
def test_get_mask_account(input_account, expected):
    assert get_mask_account(input_account) == expected


@pytest.mark.parametrize(
    "input_account",
    [
        12345,  # номер счета из 5 цифр
        123456789012345678901234567890,  # номер счета из 30 цифр
    ]
)
def test_get_mask_account_invalid_length(input_account):
    with pytest.raises(ValueError, match="Номер счета должен содержать ровно 20 цифр."):
        get_mask_account(input_account)
# tests/test_masks.py
