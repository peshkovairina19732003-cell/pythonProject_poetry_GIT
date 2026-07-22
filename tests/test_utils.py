import json
from pathlib import Path
import tempfile
import pytest

# Импортируем функцию из модуля utils
from src.utils import read_json_file


@pytest.fixture
def sample_data():
    """Возвращает тестовые данные."""
    return [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": -50}
    ]


def test_read_valid_json(sample_data):
    """
    Проверяет чтение валидного JSON-файла со списком транзакций.
    """
    # Создаём временный файл в временной директории
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "test_transactions.json"

        # Записываем тестовые данные
        file_path.write_text(json.dumps(sample_data), encoding="utf-8")

        # Читаем файл через нашу функцию
        transactions = read_json_file(str(file_path))

        # Проверки
        assert len(transactions) == 2
        assert isinstance(transactions[0], dict)
        assert transactions[0]["id"] == 1
        assert transactions[1]["amount"] == -50


def test_read_empty_file():
    """
    Проверяет поведение при чтении пустого файла.
    Должен вернуть пустой список.
    """
    # Создаём временную директорию и файл внутри неё.
    with tempfile.TemporaryDirectory() as tmp_dir:
        empty_file = Path(tmp_dir) / "empty.json"
        empty_file.write_text("", encoding="utf-8")  # Пустой файл
        result = read_json_file(str(empty_file))
        assert result == []


def test_read_non_list():
    """
    Проверяет поведение при чтении файла, который содержит не-список (например, словарь).
    Должен вернуть пустой список согласно ТЗ.
    """
    invalid_data = {
        "key": "value",
        "transactions": ["This", "is", "not", "a", "list"]
    }

    with tempfile.TemporaryDirectory() as tmp_dir:
        invalid_file = Path(tmp_dir) / "invalid.json"
        invalid_file.write_text(json.dumps(invalid_data), encoding="utf-8")
        result = read_json_file(str(invalid_file))
        assert result == []
        # По условию задачи, если это не список — возвращать пустой список


def test_read_missing_file():
    """
    Проверяет поведение при попытке прочитать несуществующий файл.
    Должен вернуть пустой список.
    """
    non_existent_file = "./nonexistent/path/to/file.json"
    result = read_json_file(non_existent_file)
    assert result == []