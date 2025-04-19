import os
import unittest
from pathlib import Path
from typing import Any, Dict, List

from src.utils_csv import read_csv_transactions, read_excel_transactions, read_transactions


class TestTransactionReaders(unittest.TestCase):
    def setUp(self) -> None:
        # Определяем корневую директорию проекта
        # Если тесты запускаются из директории tests, нужно подняться на уровень выше
        if os.path.basename(os.getcwd()) == 'tests':
            project_root = Path(os.getcwd()).parent
        else:
            project_root = Path(os.getcwd())

        # Пути к тестовым файлам относительно корня проекта
        self.csv_file_path = project_root / "Data" / "transactions.csv"
        self.excel_file_path = project_root / "Data" / "transactions_excel.xlsx"

        # Проверяем, что файлы существуют
        if not self.csv_file_path.exists():
            raise FileNotFoundError(f"Тестовый файл не найден: {self.csv_file_path}")
        if not self.excel_file_path.exists():
            raise FileNotFoundError(f"Тестовый файл не найден: {self.excel_file_path}")

    def verify_transactions(self, transactions: List[Dict[str, Any]]) -> None:
        """Проверяет корректность загруженных транзакций"""
        # Проверяем, что транзакции загружены
        self.assertGreater(len(transactions), 0)

        # Проверяем структуру данных
        first_transaction = transactions[0]
        self.assertIn('id', first_transaction)
        self.assertIn('state', first_transaction)
        self.assertIn('date', first_transaction)
        self.assertIn('amount', first_transaction)
        self.assertIn('currency_name', first_transaction)
        self.assertIn('currency_code', first_transaction)
        self.assertIn('description', first_transaction)

    def test_read_csv_transactions(self) -> None:
        """Тест чтения транзакций из CSV файла"""
        transactions = read_csv_transactions(self.csv_file_path)
        self.verify_transactions(transactions)

    def test_read_excel_transactions(self) -> None:
        """Тест чтения транзакций из Excel файла"""
        transactions = read_excel_transactions(self.excel_file_path)
        self.verify_transactions(transactions)

    def test_read_transactions_auto_detect(self) -> None:
        """Тест автоопределения формата файла"""
        # Тест для CSV
        transactions_csv = read_transactions(self.csv_file_path)
        self.verify_transactions(transactions_csv)

        # Тест для Excel
        transactions_excel = read_transactions(self.excel_file_path)
        self.verify_transactions(transactions_excel)

    def test_read_transactions_unsupported_format(self) -> None:
        """Тест обработки неподдерживаемого формата"""
        # Создаем временный путь к несуществующему файлу с неподдерживаемым расширением
        invalid_path = Path("test_file.txt")
        with self.assertRaises(ValueError):
            read_transactions(invalid_path)


if __name__ == '__main__':
    unittest.main()
