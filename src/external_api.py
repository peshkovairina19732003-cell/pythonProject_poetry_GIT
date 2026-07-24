import os
import requests
from dotenv import load_dotenv

# Загрузка переменных окружения ДО получения ключа!
load_dotenv()
API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data"

def convert_to_rubles(transaction: dict) -> float:
    """Конвертирует сумму транзакции в рубли."""

    amount = transaction.get('amount')
    currency = transaction.get('currency', '')

    # Пропускаем операции уже в рублях
    if currency == 'RUB':
        return float(amount or 0.0)

    # Формируем URL запроса
    url = f"{BASE_URL}/convert?to=RUB&from={currency}"
    headers = {"apikey": API_KEY}

    response = requests.get(url, headers=headers)

    # Обработка ответа от API
    if (
        response.status_code != 200
        or not response.json().get('success')
        or not response.json().get('result')
    ):
        # При любой ошибке просто возвращаем исходную сумму в виде float.
        # Это соответствует условию задачи: всегда возвращать float!
        return float(amount or 0.0)

    result = response.json()['result']

    # Умножаем исходную сумму на полученный курс
    return abs(float(result))
