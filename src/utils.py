import json
from typing import List, Dict


def read_json_file(file_path: str) -> List[Dict]:
    """
    Читает данные о финансовых транзакциях из JSON-файла.

    Args:
        file_path (str): Путь к файлу JSON.

    Returns:
        List[Dict]: Список словарей с данными о транзакциях.
                 Если файл пустой, содержит не-список или не найден,
                 возвращается пустой список.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Проверка, что это именно список
            if isinstance(data, list):
                return data
            else:
                print("Ошибка: содержимое файла не является списком.")
                return []

    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка при парсинге JSON в файле {file_path}.")
        return []
    