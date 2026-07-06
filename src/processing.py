# src/processing.py
from datetime import datetime
from typing import List, Dict, Any


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> Iterator[Dict[str, Any]]:
    """
    Фильтрует операции по статусу.
    """
    for operation in operations:
        if operation.get("state") == state:
            yield operation


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
