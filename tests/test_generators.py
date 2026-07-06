import pytest
from typing import List, Dict, Any
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.fixture
def all_transactions() -> List[Dict[str, Any]]:
    """
    Комплексная фикстура со всеми видами транзакций:
    - Валидные (USD, RUB)
    - С отсутствующими ключами (None, {}, пропущенные currency/operationAmount)
    """
    return [
        # --- Валидные ---
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },

        # --- Некорректные / Пограничные случаи ---
        {"id": 1},  # Вообще без operationAmount
        {"id": 2, "operationAmount": {}},  # Пустой operationAmount
        {"id": 3, "operationAmount": {"amount": "100"}},  # Нет ключа currency
        {"id": 4, "operationAmount": {"amount": "100", "currency": {}}},  # Пустой currency
    ]


# --- Тесты для filter_by_currency ---

def test_filter_by_currency_usd(all_transactions):
    """Проверяем, что находятся ВСЕ три USD транзакции."""
    usd_gen = filter_by_currency(all_transactions, "USD")
    results = list(usd_gen)
    assert len(results) == 3
    assert all(t['operationAmount']['currency']['code'] == 'USD' for t in results)


def test_filter_by_currency_rub(all_transactions):
    rub_gen = filter_by_currency(all_transactions, "RUB")
    results = list(rub_gen)
    assert len(results) == 1
    assert results[0]["id"] == 873106923


def test_filter_by_currency_handles_missing_data(all_transactions):
    """Проверяем устойчивость к плохим данным (не должно быть падений)."""
    eur_gen = filter_by_currency(all_transactions, "EUR")  # Такой валюты нет вообще
    assert list(eur_gen) == []

    empty_gen = filter_by_currency([], "USD")
    assert list(empty_gen) == []


# --- Тесты для transaction_descriptions ---

def test_transaction_descriptions(all_transactions):
    """
    Проверяем извлечение описаний для всех валидных транзакций.
    Пропускает None и пустые значения.
    """
    desc_gen = transaction_descriptions(all_transactions)

    # Список ожиданий должен соответствовать количеству валидных
    # записей description в фикстуре all_transactions (их там 4).
    expected_descs = [
        "Перевод организации",  # id: 939719570
        "Перевод со счета на счет",  # id: 142264268
        "Перевод с карты на карту",  # id: 895315941
        "Перевод со счета на счет"  # id: 873106923
    ]

    assert list(desc_gen) == expected_descs


def test_transaction_descriptions_empty():
    assert list(transaction_descriptions([])) == []


# --- Тесты для card_number_generator ---

def test_card_number_generator_small_range():
    gen = card_number_generator(1, 3)
    assert list(gen) == ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]


def test_card_number_generator_formatting():
    gen = card_number_generator(1000000000000000, 1000000000000001)
    result = next(gen)
    assert result == "1000 0000 0000 0000"