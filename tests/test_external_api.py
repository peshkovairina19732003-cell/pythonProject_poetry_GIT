import pytest
from unittest.mock import patch
from src.external_api import convert_to_rubles


@pytest.fixture
def mock_transaction_usd():
    """Фикстура для транзакции в долларах."""
    return {
        "amount": 100,
        "currency": "USD"
    }


@patch('requests.get')
def test_convert_usd(mock_get, mock_transaction_usd):
    """
    Тестирует успешную конвертацию USD -> RUB через внешний API.
    """
    # Настраиваем заглушку для успешного ответа сервера
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {'success': True, 'result': 6900.0}  # Пример курса

    result = convert_to_rubles(mock_transaction_usd)
    assert isinstance(result, float)  # Всегда должно быть число!
    assert result == 6900.0


@patch('requests.get')
def test_convert_invalid_currency(mock_get):
    """
    Тестирует неподдерживаемую валюту (например, JPY).
    Функция должна просто вернуть исходную сумму как float.
    """
    transaction = {"amount": 100, "currency": "JPY"}

    # Имитация ошибки сервера (400 Bad Request)
    mock_response = mock_get.return_value
    mock_response.status_code = 400
    mock_response.json.return_value = {}

    result = convert_to_rubles(transaction)
    assert isinstance(result, float)  # Важно! Тип float
    assert result == 100.0


@patch('requests.get')
def test_convert_no_result_in_response(mock_get):
    """
    Тестирует ситуацию, когда сервер ответил успешно (status=200),
    но в ответе нет ключа 'result'.
    Функция должна вернуть исходную сумму.
    """
    transaction = {"amount": 100, "currency": "EUR"}

    # Ответ от сервера есть, но он неполный
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {}  # Нет результата

    result = convert_to_rubles(transaction)
    assert isinstance(result, float)
    assert result == 100.0

