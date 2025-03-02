import pytest
from src.masks import get_mask_card_number

@pytest.mark.parametrize(
    "input_card, expected",
    [
        ("1234567812345678", "1234 56** **** 5678"),  # пример ожидаемого формата
        ("", ""),                                     # пустая строка
        ("1234", "1234"),                             # граничный случай (короткая строка)
    ]
)
def test_get_mask_card_number(input_card, expected):
    assert get_mask_card_number(input_card) == expected
#tests/test_masks.py

from src.masks import get_mask_account

@pytest.mark.parametrize(
    "input_account, expected",
    [
        ("12345678901234567890", "****567890"),  # пример ожидаемого формата
        ("12345", "12345"),                     # граничный случай
        ("", ""),                               # пустая строка
    ]
)
def test_get_mask_account(input_account, expected):
    assert get_mask_account(input_account) == expected
#tests/test_masks.py
