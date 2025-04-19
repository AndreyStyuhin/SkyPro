import pytest


@pytest.fixture
def transactions_list():
    """Возвращает список словарей с тестовыми данными (для модуля processing)."""
    return [
        {"state": "EXECUTED", "date": "2021-12-01 10:00:00", "amount": 100},
        {"state": "CANCELED", "date": "2021-11-15 09:30:00", "amount": 200},
        {"state": "EXECUTED", "date": "2021-12-02 15:45:00", "amount": 300},
        {"state": "PENDING", "date": "2022-01-01 00:00:00", "amount": 50},
    ]
