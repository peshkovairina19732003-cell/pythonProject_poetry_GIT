# tests/test_processing.py

import pytest
from src.processing import filter_by_state, sort_by_date

@pytest.fixture
def sample_data():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01T10:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-01T09:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-02T12:00:00"},
        {"id": 4, "state": "EXECUTED", "date": "2024-01-03T15:00:00"},
    ]

def test_filter_by_state(sample_data):
    result = list(filter_by_state(sample_data))
    assert len(result) == 3

def test_filter_by_state_specific(sample_data):
    result = list(filter_by_state(sample_data, state="CANCELED"))
    assert len(result) == 1
    assert result[0]["id"] == 2

def test_sort_by_date_descending(sample_data):
    sorted_ops = sort_by_date(sample_data, reverse=True) # <-- Было sOrted_ops (опечатка!)
    assert sorted_ops[0]["id"] == 4   # <-- Тут тоже должно быть sorted_ops
    assert sorted_ops[-1]["id"] == 2

def test_sort_by_date_ascending(sample_data):
    sorted_ops = sort_by_date(sample_data, reverse=False) # <-- Опять же sOrted_ops
    assert sorted_ops[0]["id"] == 2   # <-- Должно быть sorted_ops
    assert sorted_ops[-1]["id"] == 4  # <-- Должно быть sorted_ops