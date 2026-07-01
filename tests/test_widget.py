import pytest

from src.widget import get_date, mask_account_card

# ========================
# Тесты для функции mask_account_card
# ========================

def test_mask_account_card_account():
    """Тест: Корректная маскировка номера счета."""
    input_str = "Счет 9876543210"
    expected = "Счет **3210"
    assert mask_account_card(input_str) == expected


def test_mask_account_card_card():
    """Тест: Корректная маскировка номера карты."""
    input_str = "Visa 1234567890123456"
    expected = "Visa 1234 56** **** 3456"
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize(
    "card_type, card_number, expected",
    [
        ("MasterCard", "1111222233334444", "MasterCard 1111 22** **** 4444"),
        ("Maestro", "9876543210987654", "Maestro 9876 54** **** 7654"),
        ("Счет", "98765432109876543210", "Счет **3210"),
    ],
)
def test_mask_account_card_parametrized(card_type, card_number, expected):
    """
    Параметризованный тест: Проверка универсальности функции с разными типами карт и счетов.
    """
    input_str = f"{card_type} {card_number}"
    assert mask_account_card(input_str) == expected


# ========================
# НОВЫЙ ТЕСТ: Для достижения 100% покрытия
# ========================

def test_mask_account_card_no_number_found():
    """
    Тест: Функция вызывает ValueError, если в строке отсутствует числовой номер.
    Это покрывает ветку 'if not match:' в функции mask_account_card.
    """
    input_str = "Просто текст без номера"
    with pytest.raises(ValueError, match="В строке не найден номер"):
        mask_account_card(input_str)


# ========================
# Тесты для функции get_date
# ========================

def test_get_date_with_microseconds():
    """Тест: Обработка даты С микросекундами."""
    iso_str = "2024-03-11T02:26:18.671407"
    expected = "11.03.2024"
    assert get_date(iso_str) == expected

def test_get_date_without_microseconds():
    """Тест: Обработка даты БЕЗ микросекунд."""
    iso_str = "2024-03-11T02:26:18"
    expected = "11.03.2024"
    assert get_date(iso_str) == expected

def test_get_date_invalid_format():
    """Тест: Функция вызывает ValueError для некорректного формата даты."""
    invalid_str = "Не дата"
    with pytest.raises(ValueError):
        get_date(invalid_str)
