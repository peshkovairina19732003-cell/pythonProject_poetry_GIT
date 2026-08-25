import pytest

from src.categories import count_operations_by_categories


@pytest.fixture
def sample_data():
    return [
        {
            "id": 1,
            "description": "Перевод организации",
        },
        {
            "id": 2,
            "description": "Перевод с карты на карту",
        },
        {
            "id": 3,
            "description": "Перевод с карты на карту",
        },
        {
            "id": 4,
            "description": "Открытие вклада",
        },
    ]


def test_count_categories(sample_data):
    categories = ["Перевод организации", "Перевод с карты на карту", "Открытие вклада"]
    result = count_operations_by_categories(sample_data, categories)
    expected = {
        "Перевод организации": 1,
        "Перевод с карты на карту": 2,
        "Открытие вклада": 1,
    }
    assert result == expected


def test_count_empty_category(sample_data):
    categories = ["Оплата услуг"]
    result = count_operations_by_categories(sample_data, categories)
    expected = {"Оплата услуг": 0}
    assert result == expected
