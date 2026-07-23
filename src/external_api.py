import os
import requests
from dotenv import load_dotenv  # Загружаем переменные окружения

load_dotenv()
API_KEY = os.getenv('EXCHANGE_API_KEY')
BASE_URL = "https://api.apilayer.com/exchangerates_data"


def convert_to_rubles(transaction: dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction (dict): Словарь с данными о транзакции.
                           Обязательные ключи: amount, currency.

    Returns:
        float: Сумма в рублях.
               - Если валюта RUB, возвращается исходная сумма.
               - Если валюта USD/EUR, происходит конвертация через API.
               - Если валюта другая или возникла ошибка, возвращается исходная сумма.
    """

    # Пропускаем операции уже в рублях
    if transaction['currency'] == 'RUB':
        return float(transaction['amount'])

    # Определяем валюту для конвертации (USD или EUR)
    base_currency = transaction.get('currency', '')
    target_currency = 'RUB'

    # Формируем URL запроса
    url = f"{BASE_URL}/convert?to={target_currency}&from={base_currency}"
    headers = {"apikey": API_KEY}

    response = requests.get(url, headers=headers)

    # Обработка ответа от API
    if response.status_code != 200 or not response.json().get('success'):
        # Если статус не ОК ИЛИ сервер вернул неуспешный результат,
        # мы просто возвращаем исходную сумму в виде float.
        # Это соответствует условию задачи: всегда возвращать float!
        return float(transaction['amount'])

    data = response.json()
    result = data.get('result')  # Полученная сумма в рублях

    # Проверка на случай, если API вдруг изменит структуру ответа
    if result is None:
        return float(transaction['amount'])

    # Умножаем исходную сумму на полученный курс
    return abs(float(result))
