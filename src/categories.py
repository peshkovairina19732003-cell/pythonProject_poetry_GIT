from collections import defaultdict
from typing import Dict, Iterable, List


def count_operations_by_categories(transactions: List[Dict], categories: Iterable[str]) -> dict:
    """
    Считает количество операций по указанным категориям на основе поля description.

    Args:
        transactions (List[Dict]): Список транзакций.
        categories (Iterable[str]): Перечисление категорий для поиска.

    Returns:
        dict: Словарь вида {категория: количество}.
            Категории с нулевым количеством также будут включены в словарь.
    """
    # Создаём счётчик, который автоматически создаёт ключ со значением 0.
    counter = defaultdict(int)

    # Для быстрого поиска создаём множество категорий в нижнем регистре.
    category_set_lower = {cat.lower() for cat in categories}

    # Проходимся по каждой операции.
    for transaction in transactions:
        desc = transaction.get("description", "").lower()

        # Находим первую совпавшую категорию.
        for cat in categories:
            if cat.lower() in desc and cat.lower() in category_set_lower:
                # Записываем в словарь с оригинальным регистром.
                counter[cat] += 1
                break  # Одна операция может попасть только в одну категорию.

    # ГАРАНТИРУЕМ НАЛИЧИЕ ВСЕХ ЗАПРОШЕННЫХ КАТЕГОРИЙ!
    # Если категория не встречалась, её значение будет равно 0.
    for category in categories:
        _ = counter[category]  # Обращаемся к элементу словаря без сохранения результата.

    return dict(counter)
