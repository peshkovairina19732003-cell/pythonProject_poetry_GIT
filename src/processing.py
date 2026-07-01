from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(operations: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Принимает список словарей с данными об операциях и фильтрует их по статусу.

    Функция возвращает новый список, содержащий только те словари,
    у которых значение ключа 'state' совпадает с переданным параметром.

    Args:
        operations (List[Dict[str, Any]]): Список словарей, представляющих банковские операции.
        state (str, optional): Статус для фильтрации. По умолчанию 'EXECUTED'.

    Returns:
        List[Dict[str, Any]]: Новый список отфильтрованных операций.

    """
    return [operation for operation in operations if operation.get('state') == state]


def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по значению ключа 'date'.

    Функция принимает список операций и возвращает новый список,
    отсортированный по дате. Формат даты в словаре — ISO 8601.

    Args:
        operations (List[Dict[str, Any]]): Список словарей, представляющих операции.
        reverse (bool, optional): Порядок сортировки. True для убывания (сначала новые).
                                  False для возрастания (сначала старые). По умолчанию True.

    Returns:
        List[Dict[str, Any]]: Новый отсортированный список операций.

    """
    return sorted(operations, key=lambda op: datetime.fromisoformat(op['date']), reverse=reverse)

