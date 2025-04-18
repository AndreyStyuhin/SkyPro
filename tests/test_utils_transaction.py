from unittest.mock import patch, MagicMock
from src.utils import load_operations, convert_to_rub

# Тест для load_operations
import json


def test_load_operations():
    # Создаем временный файл с данными
    with open("test_operations.json", "w", encoding="utf-8") as f:
        json.dump([{"amount": 100, "currency": "RUB"}], f)

    # Проверяем загрузку данных
    result = load_operations("test_operations.json")
    assert result == [{"amount": 100, "currency": "RUB"}]

    # Проверяем случай с пустым файлом
    with open("empty_operations.json", "w", encoding="utf-8") as f:
        f.write("")

    result = load_operations("empty_operations.json")
    assert result == []


# Тест для convert_to_rub
@patch("requests.get")
def test_convert_to_rub(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 75.5}
    mock_get.return_value = mock_response

    result = convert_to_rub(1, "USD")
    assert result == 75.5
