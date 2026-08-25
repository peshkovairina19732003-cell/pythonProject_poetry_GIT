from unittest.mock import patch

import pytest

from src.search import search_operations_by_description


@pytest.fixture
def sample_data():
    """Возвращает примерный список транзакций."""
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {"amount": "31957.58", "currency": {"code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 159683******5199",
            "to": "Счет ****9589",
        },
        {
            "id": 2,
            "description": "Перевод с карты на карту",
        },
        {
            "id": 3,
            "description": "Открытие вклада",
        },
    ]


@patch("src.file_handlers.read_transactions_from_csv")
def test_search_valid(mock_read_csv, sample_data):
    """
    Тестирует корректную маскировку валидного номера карты.
    """
    mock_read_csv.return_value = sample_data  # Можно сразу вернуть list[dict]

    result = search_operations_by_description(sample_data, "организации")
    assert len(result) == 1
    assert result[0]["id"] == 441945886


@patch("src.file_handlers.read_transactions_from_csv")
def test_search_case_insensitive(mock_read_csv, sample_data):
    """
    Тестирует нечувствительность к регистру при поиске.
    """
    mock_read_csv.return_value = sample_data
    result = search_operations_by_description(sample_data, "ОРГАНИЗАЦИИ")
    assert len(result) == 1
    assert result[0]["id"] == 441945886


@patch("src.file_handlers.read_transactions_from_csv")
def test_search_no_match(mock_read_csv, sample_data):
    """
    Тестирует отсутствие совпадений.
    """
    mock_read_csv.return_value = sample_data
    result = search_operations_by_description(sample_data, "неизвестно")
    assert result == []
