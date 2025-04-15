# src/config.py
from os import path, makedirs
from pathlib import Path
from typing import Union

# Создаем корневую директорию проекта - explicitly type as Path
PROJECT_ROOT: Path = Path(path.dirname(path.dirname(path.abspath(__file__))))

# Путь к директории с данными
DATA_DIR: Path = PROJECT_ROOT / 'Data'


# Путь к директории с логами
LOG_DIR: Path = PROJECT_ROOT / 'logs'
makedirs(LOG_DIR, exist_ok=True)  # Создаем директорию, если ее нет

# Путь к файлу логов
LOG_FILE: Path = LOG_DIR / 'app.log'

# Настройки логирования
LOG_FORMAT: dict[str, Union[str, Path]] = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'filename': LOG_FILE,
}

# Принимаем путь к основной директории проекта
BASE_DIR: Path = Path(__file__).resolve().parent.parent  # Указатель на директорию проекта project/
