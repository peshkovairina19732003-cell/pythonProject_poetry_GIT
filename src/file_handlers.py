from typing import Dict, List

import pandas as pd


def read_transactions_from_csv(file_path: str) -> List[Dict]:
    """
    Читает финансовые операции из файла CSV.

    Args:
        file_path (str): Путь к файлу CSV.

    Returns:
        List[Dict]: Список словарей с транзакциями.
                  Если файл не найден или содержит неверный формат,
                  возвращается пустой список.
    """
    try:
        # Pandas автоматически парсит дату как строку.
        df = pd.read_csv(
            file_path,
            dtype={"amount": float},  # Сумма должна быть числом
            parse_dates=["date"],  # Дата будет строкой ISO
            encoding="utf-8",
        )

        # Преобразуем DataFrame в список словарей.
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Ошибка при чтении CSV-файла {file_path}: {e}")
        return []


def read_transactions_from_excel(file_path: str) -> List[Dict]:
    """
    Читает финансовые операции из файла Excel.

    Args:
        file_path (str): Путь к файлу Excel.

    Returns:
        List[Dict]: Список словарей с транзакциями.
                  Если файл не найден или содержит неверный формат,
                  возвращается пустой список.
    """
    try:
        # Чтение первого листа книги Excel.
        df = pd.read_excel(file_path, sheet_name=0, dtype={"amount": float}, parse_dates=["date"], engine="openpyxl")
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Ошибка при чтении Excel-файла {file_path}: {e}")
        return []
