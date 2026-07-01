from datetime import datetime

import pytest

from src.processing import filter_by_state, sort_by_date

# ========================
# Фикстуры (Fixtures)
# ========================

@pytest.fixture
def sample_operations():
    """
    Фикстура, предоставляющая базовый набор операций для тестирования.
    Содержит разные статусы и даты.
    """
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15T10:00:00.000"},
        {"id": 2, "state": "CANCELED", "date": "2023-12-25T15:30:15.123"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-16T08:45:00.000"},
        {"id": 4, "state": "PENDING", "date": "2024-02-10T12:00:00.000"},
    ]

@pytest.fixture
def operations_with_same_date():
    """
    Фикстура для тестирования сортировки, где у нескольких операций одинаковая дата.
    """
    return [
        {"id": 1, "state": "A", "date": "2024-01-15T10:00:00.000"},
        {"id": 2, "state": "B", "date": "2024-01-15T10:00:00.000"},
        {"id": 3, "state": "C", "date": "2024-01-15T10:00:00.000"},
    ]

@pytest.fixture
def empty_operations():
    """
    Фикстура с пустым списком для проверки краевых случаев.
    """
    return []

# ========================
# Тесты для функции filter_by_state
# ========================

def test_filter_by_state_default(sample_operations):
    """Тест: Фильтрация по статусу по умолчанию ('EXECUTED')."""
    result = filter_by_state(sample_operations)
    assert len(result) == 2
    assert all(op["state"] == "EXECUTED" for op in result)

def test_filter_by_state_specific(sample_operations):
    """Тест: Фильтрация по конкретному статусу ('CANCELED')."""
    result = filter_by_state(sample_operations, state="CANCELED")
    assert len(result) == 1
    assert result[0]["id"] == 2

def test_filter_by_state_no_matches(sample_operations):
    """Тест: Функция возвращает пустой список, если статус не найден."""
    result = filter_by_state(sample_operations, state="REFUNDED")
    assert result == []

def test_filter_by_state_empty_list(empty_operations):
    """Тест: Функция корректно работает с пустым входным списком."""
    result = filter_by_state(empty_operations)
    assert result == []

# ========================
# Тесты для функции sort_by_date
# ========================

def test_sort_by_date_descending(sample_operations):
    """Тест: Сортировка по убыванию дат (новые -> старые)."""
    result = sort_by_date(sample_operations) # reverse=True по умолчанию
    dates = [datetime.fromisoformat(op["date"]) for op in result]
    # Проверяем, что каждая следующая дата не больше предыдущей
    assert all(dates[i] >= dates[i+1] for i in range(len(dates)-1))

def test_sort_by_date_ascending(sample_operations):
    """Тест: Сортировка по возрастанию дат (старые -> новые)."""
    result = sort_by_date(sample_operations, reverse=False)
    dates = [datetime.fromisoformat(op["date"]) for op in result]
    # Проверяем, что каждая следующая дата не меньше предыдущей
    assert all(dates[i] <= dates[i+1] for i in range(len(dates)-1))

def test_sort_by_date_same_date(operations_with_same_date):
    """Тест: Стабильность сортировки при одинаковых датах.
       Порядок элементов с одинаковым ключом сортировки не должен меняться."""
    result = sort_by_date(operations_with_same_date)
    # Так как даты одинаковы, порядок должен быть таким же, как во входных данных
    assert [op["id"] for op in result] == [1, 2, 3]
