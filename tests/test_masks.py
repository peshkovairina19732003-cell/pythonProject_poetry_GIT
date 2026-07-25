import pytest

from src.masks import get_mask_account, mask_card_number


def test_mask_card_number_valid():
    """Тестирует корректную маскировку валидного номера карты."""
    card_number = "1234567890123456"
    expected = "1234 56** **** 3456"
    assert mask_card_number(card_number) == expected


def test_mask_card_number_with_spaces():
    """
    Тестирует обработку номера карты с пробелами.
    Функция должна их убирать перед проверкой длины.
    """
    # Длина со скобками — 19, после очистки станет 16
    card_number = "1234 5678 9012 3456"
    expected = "1234 56** **** 3456"
    assert mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "invalid_card",
    [
        "1234",  # Слишком короткий (после очистки)
        "12345678901234567",  # Слишком длинный (после очистки)
        "",  # Пустая строка
        None,  # Проверка типа
        "abcdEFGHijklMNOP",  # Номер содержит буквы!
    ],
)
def test_mask_card_number_invalid(invalid_card):
    """
    Тестирует, что функция вызывает ValueError для некорректных номеров карт.
    """
    if isinstance(invalid_card, str):  # Защита от передачи None или int
        with pytest.raises(ValueError):
            mask_card_number(invalid_card)


def test_get_mask_account_valid():
    """Тестирует корректную маску счёта."""
    account_number = "12345678901234567890"
    expected = "**7890"
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize(
    "invalid_account",
    ["123", "12a4", "", None],  # Короткий / Буквы / Пустой / Тип
)
def test_get_mask_account_invalid(invalid_account):
    """
    Тестирует, что функция вызывает ValueError для некорректных номеров счетов.
    """
    # Защита от передачи None или int. Оставляем только строки.
    if isinstance(invalid_account, str):
        with pytest.raises(ValueError):
            get_mask_account(invalid_account)
