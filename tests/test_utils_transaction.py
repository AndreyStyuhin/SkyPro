import unittest
from unittest.mock import patch, MagicMock
from src.utils import load_transactions
from src.external_api import convert_to_rub

class TestTransactions(unittest.TestCase):

    @patch('external_api.convert_to_rub')
    def test_load_transactions(self, mock_convert_to_rub):
        mock_convert_to_rub.return_value = 75.0  # Мокаем курс 1 USD = 75 RUB

        transactions = [
            {'amount': 100, 'currency': 'RUB'},
            {'amount': 1, 'currency': 'USD'},
            {'amount': 10, 'currency': 'EUR'}
        ]

        result = load_transactions(transactions)
        self.assertEqual(result, 100 + 75 + 750)  # 100 RUB + 1 USD * 75 + 10 EUR * 75

if __name__ == '__main__':
    unittest.main()