import pytest

from src.widget import mask_account_card


@pytest.mark.parametrize(
    "input_value, expected",
    [
        ("Visa Platinum 1234567812345678", "Visa Platinum 1234 56** **** 5678"),  # Маскирование карты
        ("Счет 12345678901234567890", "Счет **7890"),                           # Маскирование счёта
        (None, None),                                                           # Некорректные данные
        ("", None),                                                             # Пустая строка
    ]
)
def test_mask_account_card(input_value, expected):
    assert mask_account_card(input_value) == expected


from src.widget import get_date


@pytest.mark.parametrize(
    "input_date_str, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),  # Корректный формат даты
        ("2024-12-31T23:59:59.999999", "31.12.2024"),  # Корректный формат даты (граничное значение)
        ("2024-01-01T00:00:00.000000", "01.01.2024"),  # Корректный формат даты (начальное значение)
        ("2024-03-11", None),                          # Некорректный формат (отсутствует время)
        ("2024/03/11T02:26:18.671407", None),          # Некорректный формат (неправильный разделитель)
        ("", None),                                    # Пустая строка
        (None, None),                                  # None
    ]
)
def test_get_date(input_date_str, expected):
    assert get_date(input_date_str) == expected