def get_mask_card_number(card_number: str) -> str:
    """
    Принимает номер банковской карты и возвращает его
    в замаскированном формате XXXX XX** **** XXXX.
    Проверяет, что номер карты состоит из 16 цифр.
    """
    # 1. ПРОВЕРКА ТИПА - САМОЕ ПЕРВОЕ ДЕЙСТВИЕ!
    if not isinstance(card_number, str):
        raise ValueError("Номер карты должен быть строкой")

    # 2. Очистка от пробелов
    card_number = card_number.replace(" ", "")

    # 3. Проверка длины и содержимого
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Номер карты должен содержать ровно 16 цифр")

    part1 = card_number[:4]
    part2 = card_number[4:6] + "**"
    part3 = "****"
    part4 = card_number[-4:]

    return f"{part1} {part2} {part3} {part4}"


def get_mask_account(account_number: str) -> str:
    """
    Принимает на вход номер счета и возвращает его маску. Номер счета замаскирован
    и отображается в формате **XXXX где X — это цифра номера.
    То есть видны только последние 4 цифры номера, а перед ними — две звездочки.
    """
    # 1. ПРОВЕРКА ТИПА - САМОЕ ПЕРВОЕ ДЕЙСТВИЕ!
    if not isinstance(account_number, str):
        raise ValueError("Номер счета должен быть строкой")

    clean_account = account_number.replace(" ", "")

    if len(clean_account) < 4 or not clean_account.isdigit():
        raise ValueError("Номер счета должен содержать не менее 4 цифр")

    return f"**{clean_account[-4:]}"
