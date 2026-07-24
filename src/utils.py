import json

from typing import Dict, List


def read_json_data(json_path: str) -> List[Dict]:
    """
    Читает данные о финансовых транзакциях из строки формата JSON.

    Args:
        json_path (str): Строка с данными в формате JSON.

    Returns:
        List[Dict]: Список словарей с данными о транзакциях.
                  Если строка содержит неверный формат данных,
                  возвращается пустой список.
    """
    try:
        with open(json_path, mode='r', encoding="utf-8") as f:
            # Парсим входную строку
            data = json.load(f)

            # Проверяем тип данных
            if isinstance(data, list):
                return data
            else:
                return []

    except Exception as e:
        print(f"Ошибка парсинга JSON: {e}")
        return []
