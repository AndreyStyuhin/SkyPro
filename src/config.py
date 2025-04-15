# src/config.py
import os
from pathlib import Path

from src.utils import PROJECT_ROOT

# м корневую директорию проекта
PROJECT_ROOT = (os.path.dirname(os.path.abspath(__file__)))

# Путь к директории с данными
DATA_DIR = os.path.join(PROJECT_ROOT, 'Data')

# Путь к директории с логами
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
os.makedirs(LOG_DIR, exist_ok=True) # Создаем директорию, если ее нет

# Путь к файлу логов
LOG_FILE = os.path.join(LOG_DIR, 'app.log')

# Настройки логирования
LOG_FORMAT = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'filename': LOG_FILE,
}

# Принимаем путь к основной директории проекта

BASE_DIR = Path(__file__).resolve().parent.parent # Указатель на директорию проекта project/
DATA_DIR = BASE_DIR / 'Data' # Путь к директории с данными
