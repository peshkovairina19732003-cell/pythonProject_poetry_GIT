import os
from datetime import datetime

# Загружаем API_KEY для конвертации валют.
from dotenv import load_dotenv

from src.categories import count_operations_by_categories
from src.external_api import convert_to_rubles
from src.file_handlers import read_transactions_from_csv, read_transactions_from_excel
from src.masks import get_mask_account
from src.search import search_operations_by_description
# Импортируем наши модули
from src.utils import read_json_file

load_dotenv()
API_KEY = os.getenv("EXCHANGE_API_KEY")


def filter_transactions(
    data: list[dict],
    status: str | None = None,
    sort_date_ascending: bool | None = None,
    only_rubles: bool = False,
    search_in_desc: str | None = None,
) -> list[dict]:
    """Применяет фильтры к данным."""
    # Фильтрация по статусу (регистронезависимо).
    if status is not None:
        status_upper = status.upper()
        data = [t for t in data if t.get("state") == status_upper]

    # Конвертация сумм в рубли (если требуется). Добавляем поле rub_amount.
    # Используем генератор словарей вместо цикла + append.
    data = [
        {**trans, "rub_amount": round(convert_to_rubles(trans), 2)}
        for trans in data
        if trans.get("operationAmount", {}).get("currency", {}).get("code") != "RUB"
    ] or data  # Если нет операций с иностранной валютой, оставляем исходный список

    # Оставляем только рублёвые операции.
    if only_rubles:
        data = [t for t in data if "rub_amount" in t or ("RUB" in t.get("operationAmount", {}))]

    # Поиск по описанию.
    # Исправлено: если поисковая строка пустая, возвращаем весь список без фильтрации.
    if search_in_desc and search_in_desc.strip():
        data = search_operations_by_description(data, search_in_desc)

    # Сортирует по дате.
    if sort_date_ascending is not None:
        data.sort(key=lambda x: datetime.fromisoformat(x["date"]), reverse=(not sort_date_ascending))

    return data


def format_transaction_for_printing(transaction: dict) -> str:
    """Форматирует одну операцию для вывода в консоль."""
    date = datetime.fromisoformat(transaction["date"]).strftime("%d.%m.%Y")
    desc = transaction.get("description", "")
    from_field = get_mask_account(transaction.get("from", ""))
    to_field = get_mask_account(transaction.get("to", ""))

    amount_str = ""
    if "rub_amount" in transaction:
        amount_str = f"{transaction['rub_amount']} руб."
    else:
        amount_obj = transaction.get("operationAmount", {})
        amount_str = f"{amount_obj.get('amount')} {amount_obj.get('currency', {}).get('name')}"

    return f"{date} {desc}\n{from_field} -> {to_field}\nСумма: {amount_str}\n\n"


def main():
    """Основная логика взаимодействия с пользователем."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.\nВыберите необходимый пункт меню:")

    while True:
        file_type = input(
            "\n1. Получить информацию о транзакциях из JSON-файла\n"
            "2. Получить информацию о транзакциях из CSV-файла\n"
            "3. Получить информации о транзакциях из XLSX-файла\n"
            "Ваш выбор: "
        ).strip()

        if file_type not in ["1", "2", "3"]:
            print("Пожалуйста, выберите корректный вариант.")
            continue

        # Чтение файлов.
        if file_type == "1":
            data = read_json_file("data/operations.json")
        elif file_type == "2":
            data = read_transactions_from_csv("transactions.csv")
        else:
            data = read_transactions_from_excel("transactions_excel.xlsx")

        print(f"\nДля обработки выбран {'JSON' if file_type == '1' else 'CSV' if file_type == '2' else 'Excel'} файл.")

        # Фильтрация по статусу.
        valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
        while True:
            user_status = (
                input(
                    "\nВведите статус, по которому необходимо выполнить фильтрацию:\nДоступные статусы: EXECUTED, CANCELED, PENDING\n"
                )
                .upper()
                .strip()
            )
            if user_status in valid_statuses or user_status == "":
                break
            print(f"Статус операции \"{user_status}\" недоступен.")

        # Остальные вопросы.
        sort_answer = input("\nОтсортировать операции по дате? Да/Нет ").lower().startswith("д")
        sort_order = input("По возрастанию или по убыванию? ").lower().startswith("в")
        only_rubles = input("\nВыводить только рублевые транзакции? Да/Нет ").lower().startswith("д")
        search_answer = (
            input("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет ")
            .lower()
            .startswith("д")
        )
        search_term = input("Введите слово для фильтрации: ") if search_answer else ""

        # Применяем фильтры.
        filtered_data = filter_transactions(
            data=data,
            status=user_status or None,  # Пустая строка превращается в None
            sort_date_ascending=sort_order,
            only_rubles=only_rubles,
            search_in_desc=search_term,
        )

        # Вывод результатов.
        if len(filtered_data):
            print("\nРаспечатываю итоговый список транзакций...")
            for tr in filtered_data:
                print(format_transaction_for_printing(tr))
            print(f"Всего банковских операций в выборке: {len(filtered_data)}")
        else:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")

        # Дополнительная аналитика.
        categories = ["Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту", "Открытие вклада"]
        counts = count_operations_by_categories(filtered_data, categories)

        # Улучшено: выводим только те категории, у которых есть совпадения.
        non_empty_categories = [(cat, cnt) for cat, cnt in counts.items() if cnt > 0]
        if non_empty_categories:
            print("\nСтатистика по категориям:")
            for category, count in non_empty_categories:
                print(f"- {category}: {count}")
        else:
            print("Ни одна операция не попала ни в одну категорию.")


if __name__ == "__main__":
    main()
