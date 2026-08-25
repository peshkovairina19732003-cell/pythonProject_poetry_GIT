import re
from typing import Dict, List


def search_operations_by_description(transactions: List[Dict], search_term: str) -> List[Dict]:
    """
    Ищет операции, содержащие указанный поисковый запрос в поле description.

    Args:
        transactions (List[Dict]): Список словарей с операциями.
        search_term (str): Строка для поиска.

    Returns:
        List[Dict]: Список операций, соответствующих запросу.
    """
    # Приводим поисковую строку к нижнему регистру для нечувствительного поиска.
    pattern = re.compile(re.escape(search_term.lower()))

    return [
        transaction
        for transaction in transactions
        if "description" in transaction and pattern.search(transaction["description"].lower())
    ]
