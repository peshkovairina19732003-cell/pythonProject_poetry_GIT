import os
import requests
from dotenv import load_dotenv  # Загружаем переменные окружения

load_dotenv()
API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data"


def convert_to_rubles(transaction: dict) -> float:
    """
    Конвертирует сумму операции в рубли.

    Args:
        transaction (dict): Словарь с данными о банковской операции.
                           Обязательные поля: operationAmount.amount, operationAmount.currency.code.

    Returns:
        float: Сумма в рублях.
               - Если валюта RUB, возвращается исходная сумма.
               - При ошибке запроса к API или отсутствии ключа result
                 возвращается исходная сумма в виде числа с плавающей точкой.
    """

    # Получаем доступ к вложенным полям
    amount_str = transaction.get("operationAmount", {}).get("amount")  # Это строка! Нужно привести к числу
    currency_code = transaction.get("operationAmount", {}).get("currency", {}).get("code")  # Может быть None

    # Пропускаем операции уже в рублях
    if currency_code == "RUB":
        return float(amount_str or 0.0)

    # Формируем URL запроса
    url = f"{BASE_URL}/convert?to=RUB&from={currency_code}"
    headers = {"apikey": API_KEY}

    response = requests.get(url, headers=headers)

    # Обработка ответа от API
    if (
            response.status_code != 200
            or not response.json().get("success")
            or not response.json().get("result")
    ):
        # При любой ошибке просто возвращаем исходную сумму в виде float.
        return float(amount_str or 0.0)

    result = response.json()["result"]

    # Умножаем исходную сумму на полученный курс
    return abs(float(result))
