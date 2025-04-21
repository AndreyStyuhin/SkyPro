import logging
import traceback



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