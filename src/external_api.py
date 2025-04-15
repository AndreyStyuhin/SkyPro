import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
BASE_URL = 'https://api.apilayer.com/exchangerates_data/latest'


def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    """
    Получает текущий курс обмена между двумя валютами.

    Аргументы:
        base_currency (str): Базовая валюта (например, 'USD', 'EUR').
        target_currency (str): Целевая валюта (например, 'RUB').

    Возвращает:
        float: Курс обмена.
    """
    headers = {
        'apikey': API_KEY
    }
    params = {
        'base': base_currency,
        'symbols': target_currency
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data['rates'][target_currency]


def convert_to_rub(amount: float, currency: str) -> float:
    """
    Конвертирует сумму в рубли.

    Аргументы:
        amount (float): Сумма для конвертации.
        currency (str): Валюта суммы ('RUB', 'USD', 'EUR').

    Возвращает:
        float: Сумма в рублях.
    """
    if currency == 'RUB':
        return amount
    elif currency in ['USD', 'EUR']:
        rate = get_exchange_rate(currency, 'RUB')
        return amount * rate
    else:
        raise ValueError(f"Unsupported currency: {currency}")
