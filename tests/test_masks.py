import pytest

from src.masks import get_mask_account, get_mask_card_number

# ========================
# Тесты для функции get_mask_card_number
# ========================

def test_get_mask_card_number_valid():
    """Тест: Корректная маскировка валидного номера карты (16 цифр)."""
    card_number = "1234567890123456"
    expected = "1234 56** **** 3456"
    assert get_mask_card_number(card_number) == expected


def test_get_mask_card_number_with_spaces():
    """Тест: Функция корректно обрабатывает номер карты с пробелами."""
    # Функция убирает пробелы перед проверкой длины
    card_number = "1234 5678 9012 3456" # Длина со скобками - 19, после очистки станет 16
    expected = "1234 56** **** 3456"
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "invalid_card",
    [
        "12345",                               # Слишком короткий (после очистки)
        "12345678901234567",                  # Слишком длинный (после очистки)
        "",                                    # Пустая строка
        None,                                  # NoneType - проверка типа
        "abcdEFGHijklMNOP",                    # НОВЫЙ ТЕСТ: 16 символов, но не цифры! (проверка ветки isdigit())
    ],
)
def test_get_mask_card_number_invalid(invalid_card):
    """Тест: Функция вызывает ValueError для некорректных номеров карт."""
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_card)


# ========================
# Тесты для функции get_mask_account
# ========================

def test_get_mask_account_valid():
    """Тест: Корректная маскировка валидного номера счета."""
    account_number = "1234567890"
    expected = "**7890" # Маска из последних 4 цифр
    assert get_mask_account(account_number) == expected


def test_get_mask_account_min_length():
    """Тест: Корректная маскировка минимально допустимого номера счета (4 цифры)."""
    account_number = "1234"
    expected = "**1234"
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize(
    "invalid_account",
    [
        "123",                 # Слишком короткий (менее 4 цифр)
        "12a4",                # Содержит нецифровые символы
        "",                    # Пустая строка
        None,                  # NoneType - проверка типа
    ],
)
def test_get_mask_account_invalid(invalid_account):
    """Тест: Функция вызывает ValueError для некорректных номеров счетов."""
    with pytest.raises(ValueError):
        get_mask_account(invalid_account)
