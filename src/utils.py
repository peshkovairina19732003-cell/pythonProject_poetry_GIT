import json
import logging
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)  # Имя логера совпадает с именем модуля
logger.setLevel(logging.DEBUG)

# Настраиваем формат записи
log_format = "%(asctime)s | %(levelname)-8s | %(module)s - %(message)s"
formatter = logging.Formatter(log_format)

# Настраиваем запись в файл
file_handler = logging.FileHandler(
    filename=Path("logs", "utils.log"), mode="w"  # Путь к файлу лога  # Перезаписывать при каждом запуске
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def read_json_file(file_path: str) -> list[dict]:
    """
    Читает данные о финансовых транзакциях из файла формата JSON.

    Args:
        file_path (str): Путь к файлу JSON.

    Returns:
        List[Dict]: Список словарей с данными о транзакциях.
                  Если файл не найден / пуст / содержит неверный формат данных,
                  возвращается пустой список.
    """
    try:
        logger.info(f"Попытка прочитать файл {file_path}")

        if not Path(file_path).exists():
            logger.warning(f"Файл '{file_path}' не существует.")
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            # По условию задачи: если это не список, вернуть пустой список
            if isinstance(data, list):
                logger.debug(f"Успешно прочитано {len(data)} транзакций")
                return data
            else:
                logger.error(f"Содержимое файла '{file_path}' имеет неверный тип данных ({type(data)})")
                return []

    except Exception as e:
        logger.exception(f"Ошибка при чтении файла {file_path}: {e}")  # Запишет ошибку + трассировку стека
        return []
