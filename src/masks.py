import logging
from pathlib import Path

# === НАЧАЛО БЛОКА ЛОГИРОВАНИЯ ===
mask_logger = logging.getLogger(__name__)  # Используем имя текущего модуля
mask_logger.setLevel(logging.DEBUG)

log_format = "%(asctime)s | %(levelname)-8s | %(module)s - %(message)s"
formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler(
    filename=Path("logs", "masks.log"), mode="w"  # Файл будет перезаписываться при каждом запуске приложения
)
file_handler.setFormatter(formatter)
mask_logger.addHandler(file_handler)


# === КОНЕЦ БЛОКА ЛОГИРОВАНИЯ ===


def mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты по стандарту: первые 6 цифр видны,
    следующие 6 скрыты звёздочками, последние 4 — открыты.

    Args:
        card_number (str): Номер карты из 16 цифр (может содержать пробелы).

    Returns:
        str: Отформатированный замаскированный номер.

    Raises:
        ValueError: Если входная строка не является валидным номером карты.
    """
    mask_logger.debug(f"Маскировка номера карты: входные данные — {card_number}")

    # ПРОВЕРКА ТИПА — САМОЕ ПЕРВОЕ ДЕЙСТВИЕ!
    if not isinstance(card_number, str):
        raise ValueError("Номер карты должен быть строкой")

    # Очистка от пробелов ДО ВСЕХ проверок
    clean_number = card_number.replace(" ", "")

    # Валидация: длина И содержимое сразу вместе
    if len(clean_number) != 16 or not clean_number.isdigit():
        mask_logger.error(f"Ошибка маскировки карты '{clean_number}': Номер карты должен содержать ровно 16 цифр.")
        raise ValueError("Номер карты должен содержать ровно 16 цифр")

    part1 = clean_number[:4]
    part2 = f"{clean_number[4:6]}**"
    part3 = "****"
    part4 = clean_number[-4:]

    masked_number = f"{part1} {part2} {part3} {part4}"
    mask_logger.info(f"Карта замаскирована успешно: {masked_number}")
    return masked_number


def get_mask_account(account_number: str) -> str:
    """
    Принимает на вход номер счета и возвращает его маску.
    Номер счета замаскирован и отображается в формате **XXXX,
    где X — это цифра номера.
    То есть видны только последние 4 цифры номера, а перед ними — две звездочки.

    Args:
        account_number (str): Номер счета (минимум 4 цифры, может содержать пробелы).

    Returns:
        str: Замаскированный номер счета.

    Raises:
        ValueError: Если входная строка не является валидным номером счета.
    """
    mask_logger.debug(f"Маскировка счёта: входные данные — {account_number}")

    # ПРОВЕРКА ТИПА — САМОЕ ПЕРВОЕ ДЕЙСТВИЕ!
    if not isinstance(account_number, str):
        raise ValueError("Номер счета должен быть строкой")

    # Очистка от пробелов ДО ВСЕХ проверок
    clean_number = account_number.replace(" ", "")

    # Валидация: длина И содержимое сразу вместе
    if len(clean_number) < 4 or not clean_number.isdigit():  # Минимум 4 цифры
        mask_logger.error(f"Ошибка маскировки счёта '{clean_number}': Номер счёта должен содержать не менее 4 цифр.")
        raise ValueError("Номер счёта должен содержать не менее 4 цифр")

    masked_number = f"**{clean_number[-4:]}"  # Последние 4 цифры
    mask_logger.info(f"Счёт замаскирован успешно: {masked_number}")
    return masked_number
