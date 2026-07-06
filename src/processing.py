# src/processing.py
from datetime import datetime
from typing import List, Dict, Any


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует операции по заданному статусу.

    Args:
        operations: Список словарей с операциями.
        state: Статус для фильтрации. По умолчанию 'EXECUTED'.

    Returns:
        Новый список отфильтрованных операций.
    """
    return [op for op in operations if op.get("state") == state]


def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует операции по дате.

    Args:
        operations: Список словарей с операциями.
        reverse: Порядок сортировки. True (по умолч.) - убывание (новые сверху).

    Returns:
        Новый отсортированный список.
    """

    def get_sort_key(op):
        return datetime.fromisoformat(op["date"])

    return sorted(operations, key=get_sort_key, reverse=reverse)
