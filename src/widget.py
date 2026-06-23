from src.masks.py_module import get_mask_card_number, get_mask_account

import re

from datetime import datetime


def mask_account_card(input_str: str) -> str:
    """
    Принимает строку с типом и номером (карта или счет) и возвращает ее с замаскированным номером.
    Переиспользует функции get_mask_card_number и get_mask_account.
    """
    # Находим числовую часть в строке.
    match = re.search(r'\d{4,}', input_str)
    if not match:
        raise ValueError("В строке не найден номер")

    # Текст до номера (название) и сам номер.
    prefix = input_str[: match.start()].strip()
    number = match.group()

    # Определяем тип по префиксу.
    is_account = prefix.lower() == 'счет'

    # Применяем соответствующую функцию маскировки.
    if is_account:
        masked = get_mask_account(number)
    else:
        masked = get_mask_card_number(number)

    # Возвращаем исходный префикс и замаскированный номер.
    return f"{prefix} {masked}"


def get_date(iso_date_str: str) -> str:
    """
    Преобразует строку с датой из формата ISO "2024-03-11T02:26:18.671407"
    в формат "ДД.ММ.ГГГГ".
    """
    try:
        # Пробуем распарсить строку с микросекундами.
        dt_object = datetime.strptime(iso_date_str, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        # Если не получилось, пробуем без микросекунд.
        dt_object = datetime.strptime(iso_date_str, "%Y-%m-%dT%H:%M:%S")

    return dt_object.strftime("%d.%m.%Y")
