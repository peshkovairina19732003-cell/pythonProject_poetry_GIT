import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data():
    """
    Фикстура данных для тестирования.
    ВАЖНО: Теперь здесь ТРИ операции EXECUTED (id 1, 3, 4)
    и даты идут строго по возрастанию ID.
    """
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01T10:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-01T09:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-02T12:00:00"},
        {"id": 4, "state": "EXECUTED", "date": "2024-01-03T15:00:00"},
    ]


# --- Тесты фильтра ---
@pytest.mark.parametrize(
    "filter_state, expected_count",
    [
        ("EXECUTED", 3),  # ИСПРАВЛЕНО НА 3 (так как их три в fixture выше)
        ("CANCELED", 1),  # Только один CANCELED
        ("PENDING", 0),  # Такого статуса нет вообще
    ],
)
def test_filter_by_state(sample_data, filter_state, expected_count):
    result = filter_by_state(sample_data, state=filter_state)
    assert len(result) == expected_count


# --- Тесты сортировки ---
@pytest.mark.parametrize(
    "reverse_sort, first_id, last_id",
    [
        # При reverse=True (убывание): сначала самые новые даты
        # Самая новая дата это id=4 (15:00), самая старая это id=2 (09:00)
        (True, 4, 2),  # ИСПРАВЛЕНО: последний теперь id=2, так как он самый ранний утром

        # При возрастании (старые -> новые): первый самый старый (id=2 - 09:00), последний новый (id=4 - 15:00)
        (False, 2, 4),
    ],
)
def test_sort_by_date(sample_data, reverse_sort, first_id, last_id):
    """
    Проверяем порядок элементов после сортировки по дате.
    Обратите внимание: время влияет на результат!
    """
    sorted_ops = sort_by_date(sample_data, reverse=reverse_sort)

    assert sorted_ops[0]["id"] == first_id
    assert sorted_ops[-1]["id"] == last_id
