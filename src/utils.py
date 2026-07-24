import json
from pathlib import Path
from typing import List, Dict


def read_json_data(json_string: str) -> List[Dict]:
    """
    Читает данные о финансовых транзакциях из строки формата JSON.

    Args:
        json_string (str): Строка с данными в формате JSON.

    Returns:
        List[Dict]: Список словарей с данными о транзакциях.
                  Если строка содержит неверный формат данных,
                  возвращается пустой список.
    """
    try:
        # Парсим входную строку
        data = json.loads(json_string)

        # Проверяем тип данных
        if isinstance(data, list):
            return data
        else:
            return []

    except Exception as e:
        print(f"Ошибка парсинга JSON: {e}")
        return []