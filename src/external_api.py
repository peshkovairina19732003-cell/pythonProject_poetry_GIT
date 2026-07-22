import os
import requests
from dotenv import load_dotenv
from typing import Optional

# Загружаем токен из .env
load_dotenv()
API_KEY = os.getenv('EXCHANGE_API_KEY')
BASE_URL = "https://api.apilayer.com/exchangerates_data"


def convert_to_rubles(transaction: dict) -> Optional[float]:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction (dict): Словарь с данными о транзакции.
                           Должны присутствовать ключи amount, currency.

    Returns:
        float | None: Сумма в рублях или None, если валюта не поддерживается.
    """
    # Пропускаем операции уже в RUB
    if transaction['currency'] == 'RUB':
        return transaction['amount']

    # Определяем валюту для конвертации (USD или EUR)
    base_currency = transaction.get('currency')
    target_currency = 'RUB'

    # Формируем URL запроса
    url = f"{BASE_URL}/convert?to={target_currency}&from={base_currency}"
    headers = {"apikey": API_KEY}

    response = requests.get(url, headers=headers)

    # Обработка ответа от API
    if response.status_code == 200:
        data = response.json()
        result = data.get('result')

        # Умножаем исходную сумму на полученный курс
        if result is not None and transaction['amount']:
            return abs(float(result))

    print(f"Не удалось получить курс для {base_currency}")
    return None
