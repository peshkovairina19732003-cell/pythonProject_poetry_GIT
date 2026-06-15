def get_mask_card_number(card_number: str) -> str:
    """Принимает номер банковской карты и возвращает его
    в замаскированном формате XXXX XX** **** XXXX.
    Проверяет, что номер карты состоит из 16 цифр."""
    if len(card_number) != 16 or not card_number.isdigit():
        # Номер карты должен содержать 16 цифр
        raise ValueError
    # Формируем маску: первые 6, затем 2 звезды, затем 4 звезды, затем последние 4
    part1 = card_number[:4]
    part2 = card_number[4:6] + "**"
    part3 = "****"
    part4 = card_number[-4:]
    # Собираем результат с пробелами
    return f"{part1} {part2} {part3} {part4}"


def get_mask_account(account_number: str) -> str:
    """Принимает на вход номер счета и возвращает его маску. Номер счета замаскирован
    и отображается в формате **XXXX где X — это цифра номера.
    То есть видны только последние 4 цифры номера, а перед ними — две звездочки."""
    account_number = account_number.replace(" ", "")
    # Проверяем, что номер счёта не короче 4 цифр
    if len(account_number) < 4 or not account_number.isdigit():
    # Номер счёта должен содержать не менее 4 цифр
        raise ValueError
    # Маска: две звезды и последние 4 цифры
    return f"**{account_number[-4:]}"
