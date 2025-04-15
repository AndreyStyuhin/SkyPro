import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Union

import requests
from dotenv import load_dotenv

# Настройка логгера должна быть ДО всех функций
PROJECT_ROOT: Path = Path(__file__).parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)  # Устанавливаем уровень

# Очищаем существующие handlers
logger.handlers = []

# Создаем и настраиваем handler
file_handler = logging.FileHandler(LOG_DIR / "utils.log", mode="w")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)

# Добавляем handler к логгеру
logger.addHandler(file_handler)

# Также добавим вывод в консоль для отладки
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info("Логгер успешно инициализирован")  # Тестовое сообщение


def load_operations(path: str) -> List[Dict[str, Any]]:
    """Загружает данные о транзакциях из JSON-файла"""
    try:
        logger.info(f"Попытка загрузить файл: {path}")

        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            if not isinstance(data, list):
                logger.warning(f"Файл {path} не содержит список!")
                return []

            logger.info(f"Успешно загружено {len(data)} операций")
            return data

    except FileNotFoundError:
        logger.error(f"Файл не найден: {path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка JSON в файле: {path}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {type(e).__name__}: {str(e)}")
        return []


load_dotenv()


def convert_to_rub(amount: Union[int, float], currency: str) -> float:
    """Конвертирует сумму в рубли"""
    try:
        logger.debug(f"Начало конвертации: {amount} {currency}")

        if currency == "RUB":
            logger.debug("Валюта уже в RUB, конвертация не нужна")
            return float(amount)

        api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        if not api_key:
            logger.critical("Отсутствует API ключ!")
            raise ValueError("API ключ не найден")

        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
        headers = {"apikey": api_key}

        logger.info(f"Запрос к API: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        logger.debug(f"Ответ API: {data}")

        if "result" not in data:
            logger.error(f"Неожиданный ответ API: {data}")
            raise ValueError("Неверный формат ответа")

        result = float(data["result"])
        logger.info(f"Конвертация успешна: {amount} {currency} = {result} RUB")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка запроса: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Ошибка конвертации: {type(e).__name__}: {str(e)}")
        raise


# Тестовый вызов для проверки логирования
if __name__ == "__main__":
    logger.info("Запуск тестового сценария")

    # Тест загрузки операций
    test_path = str(PROJECT_ROOT / "data" / "operations.json")
    operations = load_operations(test_path)
    logger.info(f"Загружено операций: {len(operations)}")

    # Тест конвертации (используем mock в реальных тестах)
    try:
        rub_amount = convert_to_rub(100, "USD")
        logger.info(f"Тест конвертации: 100 USD = {rub_amount} RUB")
    except Exception as e:
        logger.error(f"Тест конвертации провален: {str(e)}")

    logger.info("Тестовый сценарий завершен")
