import pytest
from src.processing import filter_by_state

def test_filter_by_state_executed(transactions_list):
    result = filter_by_state(transactions_list, "EXECUTED")
    assert len(result) == 2  # Предполагаем, что в фикстуре 2 записи со state="EXECUTED"
    for item in result:
        assert item["state"] == "EXECUTED"

def test_filter_by_state_none(transactions_list):
    """Проверяем случай, когда нет ни одной записи с нужным статусом."""
    result = filter_by_state(transactions_list, "NON_EXISTENT_STATE")
    assert len(result) == 0

def test_filter_by_state_empty_list(transactions_list):
    """Проверяем случай, когда список пустой."""
    result = filter_by_state([], "EXECUTED")
    assert len(result) == 0

#tests/test_processing.py

from src.processing import sort_by_date

def test_sort_by_date_desc(transactions_list):
    """Проверяем сортировку по убыванию даты."""
    sorted_transactions = sort_by_date(transactions_list, reverse=True)
    # Сравниваем даты двух первых элементов, чтобы проверить убывающий порядок
    assert sorted_transactions[0]["date"] >= sorted_transactions[1]["date"]
    assert sorted_transactions[1]["date"] >= sorted_transactions[2]["date"]

def test_sort_by_date_asc(transactions_list):
    """Проверяем сортировку по возрастанию даты."""
    sorted_transactions = sort_by_date(transactions_list, reverse=False)
    assert sorted_transactions[0]["date"] <= sorted_transactions[1]["date"]
    assert sorted_transactions[1]["date"] <= sorted_transactions[2]["date"]

#tests/test_processing.py

@pytest.mark.parametrize("test_input,expected", [
    ([{"date": "2019-08-26"}, {"date": "2019-07-03"}], ["2019-08-26", "2019-07-03"]),
    ([{"date": "2019-08-26"}, {"date": "2019-08-26"}], ["2019-08-26", "2019-08-26"]),
])
def test_sort_by_date_parametrized(test_input, expected):
    result = sort_by_date(test_input, reverse=True)
    assert len(result) == len(test_input)
    assert [x["date"] for x in result] == expected

def test_filter_by_state_none_input():
    with pytest.raises(TypeError):
        filter_by_state(None, "EXECUTED")

def test_sort_by_date_empty_dates():
    transactions = [{"date": ""}, {"date": None}]
    with pytest.raises(ValueError):
        sort_by_date(transactions)

