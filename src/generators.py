from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Генератор-фильтр транзакций по заданному коду валюты (например, 'USD').

    Функция принимает список словарей-транзакций и возвращает итератор,
    который выдает только те транзакции, у которых валюта совпадает с указанной.

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций.
        currency_code (str): Код валюты для фильтрации (например, 'USD', 'RUB').

    Yields:
        Dict[str, Anys]: Следующая транзакция, соответствующая валюте.
    """
    for transaction in transactions:
        # Используем .get() для безопасного доступа к вложенным ключам
        operation_amount = transaction.get('operationAmount')
        if not operation_amount:
            continue

        currency_info = operation_amount.get('currency')
        if not currency_info:
            continue

        if currency_info.get('code') == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор описаний транзакций.

    Принимает список транзакций и последовательно возвращает значение ключа 'description'
    из каждой транзакции.

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций.

    Yields:
        str: Описание следующей транзакции.
    """
    for transaction in transactions:
        description = transaction.get('description')
        if description is not None:
            yield description


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в заданном диапазоне.

    Генерирует номера карт в формате "XXXX XXXX XXXX XXXX" из целых чисел
    в диапазоне [start, end].

    Args:
        start (int): Начальное число диапазона (включительно).
        end (int): Конечное число диапазона (включительно).

    Yields:
        str: Следующий номер карты в отформатированном виде.
    """
    format_string = "{:016d}"  # Форматируем число до 16 знаков с ведущими нулями

    for i in range(start, end + 1):
        formatted_number = format_string.format(i)
        # Добавляем пробелы каждые 4 цифры
        spaced_number = f"{formatted_number[:4]} {formatted_number[4:8]} {formatted_number[8:12]} {formatted_number[12:]}"
        yield spaced_number
