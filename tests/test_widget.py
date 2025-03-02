import pytest
from src.widget import mask_account_card

@pytest.mark.parametrize(
    "input_value, expected",
    [
        ("1234567812345678", "1234 56** **** 5678"),  # Маскирование карты
        ("12345678901234567890", "****567890"),       # Маскирование счёта
        (None, None),                                 # Некорректные данные
        ("", ""),                                     # Пустая строка
    ]
)
def test_mask_account_card(input_value, expected):
    assert mask_account_card(input_value) == expected


from src.widget import get_date

@pytest.mark.parametrize(
    "input_date_str, expected",
    [
        ("2021-12-01 10:00:00", "01.12.2021"),  # Проверяем форматирование в нужный вид
        ("2021/12/01 10:00:00", None),         # Некорректный формат — что делает функция?
        (None, None),                          # Нет даты
    ]
)
def test_get_date(input_date_str, expected):
    assert get_date(input_date_str) == expected