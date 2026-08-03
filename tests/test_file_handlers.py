from unittest.mock import patch

import pandas as pd
import pytest

# Импортируем наши новые функции
from src.file_handlers import read_transactions_from_csv, read_transactions_from_excel


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
            "to": "Счет 646864****9589",
        }
    ]


# Тесты для CSV
@patch("pandas.read_csv")  # Подменяем функцию pandas
def test_read_csv_valid(mock_read_csv, sample_data):
    """Тестирует корректное чтение валидного CSV."""
    # Создаём DataFrame из наших тестовых данных
    df = pd.DataFrame(sample_data)
    mock_read_csv.return_value = df

    result = read_transactions_from_csv("fake_path.csv")
    assert len(result) == len(sample_data), "Количество транзакций должно совпадать."
    assert isinstance(result[0], dict), "Результат должен быть списком словарей."


@patch("pandas.read_csv")
def test_read_csv_invalid(mock_read_csv):
    """Тестирует обработку ошибки при чтении CSV."""
    mock_read_csv.side_effect = FileNotFoundError()
    result = read_transactions_from_csv("nonexistent.csv")
    assert result == [], "При ошибке чтения функция должна вернуть пустой список."


# Аналогичные тесты для Excel
@patch("pandas.read_excel")
def test_read_excel_valid(mock_read_excel, sample_data):
    """Тестирует корректное чтение валидного Excel."""
    df = pd.DataFrame(sample_data)
    mock_read_excel.return_value = df

    result = read_transactions_from_excel("fake_path.xlsx")
    assert len(result) == len(sample_data)
    assert isinstance(result[0], dict)


@patch("pandas.read_excel")
def test_read_excel_invalid(mock_read_excel):
    """Тестирует обработку ошибки при чтении Excel."""
    mock_read_excel.side_effect = ValueError()  # Любая ошибка от pandas
    result = read_transactions_from_excel("corrupted.xlsx")
    assert result == []
