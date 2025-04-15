import logging
from pathlib import Path


# Настройка логгера для модуля masks
def setup_logger():

    # Получаем путь к текущему файлу (masks.py)
    current_file = Path(__file__)

    # Получаем путь к корню проекта (поднимаемся на уровень выше src)
    project_root = current_file.parent.parent

    # Создаем директорию для логов, если она не существует
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Путь к файлу логов
    log_file = logs_dir / "masks.log"

    logger = logging.getLogger("masks")
    logger.setLevel(logging.INFO)

    # Очистка handlers чтобы избежать дублирования
    if logger.handlers:
        logger.handlers = []

    # Файловый handler с перезаписью файла
    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


logger = setup_logger()


def get_mask_card_number(card_number: int) -> str:
    """Возвращает маскированный номер карты в формате: XXXX XX** **** XXXX. Отображаются первые 6 цифр (4+2),
    следующие 2 цифры заменяются на "**", за ними следуют ещё 4 скрытые цифры "****",
    и последние 4 цифры номера отображаются без маски.
    :param card_number: Номер банковской карты в виде целого числа.
    :return: Маскированный номер карты в виде строки."""

    try:
        card_str = str(card_number)
        if len(card_str) != 16:
            error_msg = "Номер карты должен содержать ровно 16 цифр."
            logger.error(error_msg)
            raise ValueError(error_msg)

        masked_card = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
        logger.info(f"Успешно замаскирован номер карты: {masked_card}")
        return masked_card

    except Exception as e:
        logger.error(f"Ошибка при маскировании номера карты: {str(e)}")
        raise


def get_mask_account(account_number: int) -> str:
    """Возвращает маскированный номер счета в формате: **XXXX.
    Отображаются последние 4 цифры, а первые 2 цифры заменяются на "**".
    :param account_number: Номер счета в виде целого числа.
    :return: Маскированный номер счета в виде строки."""

    try:
        account_str = str(account_number)
        if len(account_str) != 20:
            error_msg = "Номер счета должен содержать ровно 20 цифр."
            logger.error(error_msg)
            raise ValueError(error_msg)

        masked_account = f"**{account_str[-4:]}"
        logger.info(f"Успешно замаскирован номер счета: {masked_account}")
        return masked_account

    except Exception as e:
        logger.error(f"Ошибка при маскировании номера счета: {str(e)}")
        raise


if __name__ == "__main__":
    print(get_mask_card_number(7000792289606361))
    print(get_mask_account(11234567890123456789))
