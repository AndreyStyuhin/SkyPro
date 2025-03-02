from src.widget import get_date


def test_get_date():
    assert get_date("2018-07-11 02:26:18") == "11.07.2018"
    assert get_date("invalid date") is None
