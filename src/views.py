import pandas as pd
from datetime import datetime
import json
import requests
from typing import Dict, List, Tuple, Optional
import os

from tests.test_generators import transactions

# Конфигурация API
EXCHANGE_RATE_API = "https://api.exchangerate-api.com/v4/latest/RUB"
EXCHANGE_API_KEY = "59a1870da0d44ce8c0ffeae7"
ALPHA_VANTAGE_API_KEY = "YOUR_ALPHA_VANTAGE_KEY"  # Нужно получить свой ключ


def load_user_settings() -> Dict:
    """Загружает пользовательские настройки из файла."""
    try:
        with open('user_settings.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки настроек: {e}")
        return {"user_currencies": [], "user_stocks": []}


def init_operations_file():
    """Создает шаблонный файл операций, если он отсутствует."""
    sample_data = {
        "Дата операции": ["01.01.2023", "02.01.2023"],
        "Дата платежа": ["01.01.2023", "02.01.2023"],
        "Номер карты": ["1234", "5678"],
        "Статус": ["OK", "OK"],
        "Сумма операции": [1000, 2000],
        "Валюта операции": ["RUB", "RUB"],
        "Сумма платежа": [1000, 2000],
        "Валюта платежа": ["RUB", "RUB"],
        "Кешбэк": [10, 20],
        "Категория": ["Еда", "Транспорт"],
        "MCC": [5812, 4111],
        "Описание": ["Ресторан", "Такси"],
        "Бонусы": [10, 20],
        "Округление на Инвесткопилку": [0, 0],
        "Сумма операции с округлением": [1000, 2000]
    }
    try:
        os.makedirs('data', exist_ok=True)
        df = pd.DataFrame(sample_data)
        df.to_excel('data/operations.xlsx', index=False)
        print("Создан шаблонный файл операций: data/operations.xlsx")
        return df
    except Exception as e:
        print(f"Не удалось создать файл операций: {e}")
        return pd.DataFrame()


def load_operations_data(date_range: Tuple[str, str]) -> Optional[pd.DataFrame]:
    """Загружает данные операций за указанный период."""
    try:
        file_path = 'data/operations.xlsx'

        if not os.path.exists(file_path):
            print("Файл операций не найден, создаем шаблонный...")
            return init_operations_file()

        df = pd.read_excel(file_path)

        # Парсим даты с учетом возможного времени
        datetime_formats = ["%d.%m.%Y %H:%M:%S", "%d.%m.%Y"]
        df['Дата операции'] = pd.to_datetime(
            df['Дата операции'],
            format="mixed",
            dayfirst=True,
            errors='coerce'
        )

        # Парсим входной диапазон дат
        start_date = pd.to_datetime(
            date_range[0],
            format="mixed",
            dayfirst=True,
            errors='coerce'
        )
        end_date = pd.to_datetime(
            date_range[1],
            format="mixed",
            dayfirst=True,
            errors='coerce'
        )

        if pd.isna(start_date) or pd.isna(end_date):
            raise ValueError("Некорректный формат даты в диапазоне")

        mask = (df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)
        return df.loc[mask]
    except Exception as e:
        print(f"Ошибка загрузки данных операций: {e}")
        return None


def get_date_range(input_datetime: str) -> Tuple[str, str]:
    """Возвращает диапазон дат с начала месяца по входящую дату+время."""
    try:
        # Парсим дату и время
        dt = datetime.strptime(input_datetime, "%d.%m.%Y %H:%M:%S")
        start_date = dt.replace(day=1, hour=0, minute=0, second=0)
        return start_date.strftime("%d.%m.%Y %H:%M:%S"), input_datetime
    except ValueError:
        # Пробуем парсить только дату, если время не указано
        try:
            dt = datetime.strptime(input_datetime, "%d.%m.%Y")
            start_date = dt.replace(day=1)
            return start_date.strftime("%d.%m.%Y"), input_datetime
        except ValueError as e:
            raise ValueError("Некорректный формат даты. Используйте ДД.ММ.ГГГГ [ЧЧ:ММ:СС]")


def fetch_currency_rates(currencies: List[str]) -> Dict[str, float]:
    """Получает текущие курсы валют."""
    rates = {}
    try:
        response = requests.get(f"{EXCHANGE_RATE_API}?api_key={EXCHANGE_API_KEY}")
        response.raise_for_status()
        data = response.json()

        for currency in currencies:
            if currency in data.get('rates', {}):
                rates[currency] = data['rates'][currency]
    except Exception as e:
        print(f"Ошибка получения курсов валют: {e}")
    return rates


def fetch_stock_prices(stocks: List[str]) -> Dict[str, float]:
    """Получает текущие цены акций."""
    prices = {}
    try:
        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={ALPHA_VANTAGE_API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if 'Global Quote' in data:
                prices[stock] = float(data['Global Quote']['05. price'])
    except Exception as e:
        print(f"Ошибка получения цен акций: {e}")
    return prices


def generate_main_page_data(df: pd.DataFrame, currencies: List[str], stocks: List[str]) -> Dict:
    """Генерирует данные для главной страницы."""
    if df is None or df.empty:
        return {"error": "No data available"}

    # Основные метрики
    total_spent = df['Сумма платежа'].sum()
    avg_transaction = df['Сумма платежа'].mean()
    total_cashback = df['Кешбэк'].sum()

    # Топ категорий
    top_categories = df.groupby('Категория')['Сумма платежа'].sum().nlargest(3).to_dict()

    # Топ транзакции
    top_transactions = df.nlargest(3, 'Сумма платежа')[['Дата операции', 'Категория', 'Сумма платежа']]
    top_transactions = top_transactions.to_dict('records')

    # Курсы валют и цены акций
    currency_rates = fetch_currency_rates(currencies)
    stock_prices = fetch_stock_prices(stocks)

    return {
        "period": f"{df['Дата операции'].min().strftime('%d.%m.%Y')} - {df['Дата операции'].max().strftime('%d.%m.%Y')}",
        "total_spent": total_spent,
        "avg_transaction": avg_transaction,
        "total_cashback": total_cashback,
        "top_categories": top_categories,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }


def display_main_page() -> None:
    """Отображает главную страницу с аналитикой."""
    print("\n=== Главная страница ===")

    # Запрос даты и времени у пользователя
    input_datetime = input("Введите дату (и время) в формате ДД.ММ.ГГГГ [ЧЧ:ММ:СС] (например 20.05.2020 16:44:00): ")

    try:
        # Получаем диапазон дат
        date_range = get_date_range(input_datetime)

        # Загружаем настройки пользователя
        settings = load_user_settings()
        currencies = settings.get("user_currencies", [])
        stocks = settings.get("user_stocks", [])

        # Загружаем данные операций
        operations_df = load_operations_data(date_range)

        # Генерируем данные для страницы
        page_data = generate_main_page_data(operations_df, currencies, stocks)

        # Выводим результаты
        print("\nАналитика за период:", page_data.get("period"))
        print(f"\nОбщие расходы: {page_data.get('total_spent', 0):.2f} RUB")
        print(f"Средний чек: {page_data.get('avg_transaction', 0):.2f} RUB")
        print(f"Общий кешбэк: {page_data.get('total_cashback', 0):.2f} RUB")

        # ... остальной вывод без изменений ...

    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    input("\nНажмите Enter чтобы вернуться в меню...")


def display_events_page() -> None:
    """Отображает страницу событий."""
    print("\n=== События ===")
    # Здесь можно реализовать аналогичную логику для событий
    input("\nНажмите Enter чтобы вернуться в меню...")


def display_cashback_categories():
    """Отображает выгодные категории повышенного кешбэка."""
    try:
        logging.info("Запуск функции display_cashback_categories")

        # Получение входных данных от пользователя
        year = int(input("Введите год для расчета: "))
        month = int(input("Введите месяц для расчета (1-12): "))

        # Здесь должен быть код получения транзакций
        # Логируем каждый шаг
        logging.info(f"Получены входные данные: год={year}, месяц={month}")

        # Вызов сервиса
        from src.services import get_cashback_categories
        result = get_cashback_categories(year, month, transactions)

        # Вывод результата
        print("\nРезультат:")
        print(result)

    except Exception as e:
        logging.error(f"Ошибка в display_cashback_categories: {e}")
        logging.error(traceback.format_exc())
        print(f"\nПроизошла ошибка: {e}")
        print("Подробности записаны в лог.")

def display_investment_page() -> None:
    """Отображает страницу инвесткопилки."""
    print("\n=== Инвесткопилка ===")
    # Реализация вывода инвесткопилки
    input("\nНажмите Enter чтобы вернуться в меню...")

def display_simple_search() -> None:
    """Отображает простой поиск."""
    print("\n=== Простой поиск ===")
    # Реализация простого поиска
    input("\nНажмите Enter чтобы вернуться в меню...")

def display_phone_search() -> None:
    """Отображает поиск по телефонным номерам."""
    print("\n=== Поиск по телефонным номерам ===")
    # Реализация поиска по телефонам
    input("\nНажмите Enter чтобы вернуться в меню...")

def display_person_transfers_search() -> None:
    """Отображает поиск переводов физическим лицам."""
    print("\n=== Поиск переводов физическим лицам ===")
    # Реализация поиска переводов
    input("\nНажмите Enter чтобы вернуться в меню...")