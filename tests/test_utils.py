import json  # Для работы со строками
from unittest.mock import patch

import pytest

from src.utils import read_json_data  # Обратите внимание на новое имя

# from io import StringIO      # Больше не нужно!


@pytest.fixture
def sample_data():
    """Возвращает примерный список транзакций."""
    return [{"id": 1, "amount": 100}, {"id": 2, "amount": -50}]


# Тест на чтение пустого списка или несуществующего файла
# МЫ БОЛЬШЕ НЕ ИМИТИРУЕМ ФАЙЛОВУЮ СИСТЕМУ!
def test_read_empty_file():
    """
    Проверяет поведение при чтении пустого файла или файла со списком [].
    Должен вернуть пустой список.
    """
    result = read_json_data("[]")  # Передаем валидную пустую структуру
    assert result == [], "Функция должна всегда возвращать только списки!"


# Основной тест на валидный JSON
def test_read_valid_json(sample_data):
    """
    Проверяет чтение валидного JSON-файла со списком транзакций.
    """
    # Преобразуем наши тестовые данные в строку JSON
    file_content = json.dumps(sample_data)

    transactions = read_json_data(file_content)
    assert len(transactions) == 2  # В списке должно быть две транзакции
    assert isinstance(transactions[0], dict)  # Первая транзакция должна быть словарём
    assert transactions[0]["id"] == 1  # ID первой транзакции должен быть равен 1


# Тест на неверную структуру данных
def test_read_non_list():
    """
    Проверяет обработку файла, который содержит не-список.
    По условию задачи функция должна вернуть пустой список.
    """
    # Имитируем словарь вместо списка
    file_content = '{"key": "value"}'

    result = read_json_data(file_content)
    assert result == [], "Функция должна возвращать только списки!"
