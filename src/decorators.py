import logging
import os
from datetime import datetime
from typing import Any, Callable, TypeVar



# Настройка логирования
def setup_logger(filename: str | None = None) -> logging.Logger:
    """
    Настраивает логгер для записи в файл или вывода в консоль.

    Параметры:
    - filename (str | None): Имя файла для записи логов. Если None, логи выводятся в консоль.

    Возвращает:
    - logger (logging.Logger): Настроенный объект логгера.
    """
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(message)s")

    # Удаляем существующие обработчики, чтобы избежать дублирования ведения журнала
    logger.handlers.clear()

    if filename is not None:
        log_file = os.path.join("logs", filename)
        os.makedirs(os.path.dirname(log_file), exist_ok=True)  # Создание папки, если не существует
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


# Декоратор для логирования вызовов функции
def log(filename: str | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для логирования вызовов функции.

    Этот декоратор записывает информацию о вызовах обернутой функции, включая
    переданные аргументы и возвращаемое значение, в указанный файл или выводит
    в консоль. В случае возникновения исключения декоратор также записывает
    информацию об ошибке.

    Параметры:
    - filename (str | None): Имя файла, в который будет записываться лог. Если не указано,
      лог выводится в консоль.

    Возвращает:
    - decorator (function): Функцию-декоратор, которая оборачивает целевую функцию.
    """
    logger = setup_logger(filename)
    R = TypeVar("R")

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        def wrapper(*args: Any, **kwargs: Any) -> R:
            function_name = func.__name__
            start_time = datetime.now()
            logger.info(f"{function_name} called at {start_time.isoformat()} with args: {args} and kwargs: {kwargs}")

            try:
                result = func(*args, **kwargs)
                logger.info(f"{function_name} result: {result}")
                return result
            except Exception as e:
                error_message = f"{function_name} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                logger.error(error_message)
                raise

        return wrapper

    return decorator
