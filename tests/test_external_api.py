import pytest
from unittest.mock import patch
from src.external_api import convert_to_rubles

@pytest.fixture
def mock_transaction_usd():
    return {
        "amount": 100,
        "currency": "USD"
    }

@patch('requests.get')
def test_convert_usd(mock_get, mock_transaction_usd):
    """
    Тестирует конвертацию USD -> RUB.
    """
    # Настраиваем заглушку для успешного ответа от API
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {'success': True, 'result': 7349.65}
    # Пример курса

    # Проверяем результат напрямую через assert
    assert convert_to_rubles(mock_transaction_usd) == 7349.65

