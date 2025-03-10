import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Фикстура для тестовых транзакций
@pytest.fixture
def transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


# Тестирование функции filter_by_currency
def test_filter_by_currency(transactions):
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 3  # Должно быть 3 транзакции с USD
    assert {t["id"] for t in usd_transactions} == {939719570, 142264268, 895315941}

    rub_transactions = list(filter_by_currency(transactions, "RUB"))
    assert len(rub_transactions) == 2  # Должно быть 2 транзакции с RUB
    assert {t["id"] for t in rub_transactions} == {873106923, 594226727}

    empty_transactions = list(filter_by_currency([], "USD"))
    assert len(empty_transactions) == 0  # Пустой список, должно быть 0 транзакций

    no_currency_transactions = list(filter_by_currency(transactions, "GBP"))
    assert len(no_currency_transactions) == 0  # Нет транзакций в GBP


# Тестирование функции transaction_descriptions
def test_transaction_descriptions(transactions):
    descriptions = list(transaction_descriptions(transactions))
    assert len(descriptions) == 5  # Должно быть 5 описаний

    expected_descriptions = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    assert descriptions == expected_descriptions

    # Тестируем пустой список
    empty_descriptions = list(transaction_descriptions([]))
    assert len(empty_descriptions) == 0  # Пустой список, должно быть 0 описаний


# Тестирование генератора card_number_generator
@pytest.mark.parametrize(
    "start, end, expected",
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (5, 5, ["0000 0000 0000 0005"]),
        (99999999, 100000000, ["0000 0000 9999 9999", "0000 0001 0000 0000"]),
        (100, 102, ["0000 0000 0000 0100", "0000 0000 0000 0101", "0000 0000 0000 0102"]),
    ],
)
def test_card_number_generator(start, end, expected):
    generated_numbers = list(card_number_generator(start, end))
    assert generated_numbers == expected

    # Проверка обработки крайних значений
    assert list(card_number_generator(99999999, 100000000)) == ["0000 0000 9999 9999", "0000 0001 0000 0000"]
    assert list(card_number_generator(1, 0)) == []  # Если диапазон неправильный, должен быть пустой список