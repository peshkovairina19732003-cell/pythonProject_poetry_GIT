# ** Проект "Банковские операции" **

## Описание
Проект представляет собой набор утилит для обработки данных о банковских операциях. Он позволяет фильтровать операции по статусу и сортировать их по дате, что является основой для клиентского виджета.

## Установка
### Клонируйте репозиторий:
~~~ 
bash
~~~

~~~
git clone <ссылка_на_ваш_репозиторий>
### Создайте виртуальное окружение:
bash
~~~

~~~
python -m venv venv
~~~
### Активируйте окружение и установите зависимости:
~~~
bash
~~~

#### Для Linux/macOS:
~~~
source venv/bin/activate
~~~
#### Для Windows:
~~~
.\venv\Scripts\activate
~~~
~~~
pip install -r requirements.txt
~~~
## Использование
### Основной функционал реализован в модуле src/processing.py.

### Фильтрация по статусу (filter_by_state)
Функция отбирает операции с заданным статусом.

~~~
from src.processing import filter_by_state

operations = [{'id': 1, 'state': 'EXECUTED'}, {'id': 2, 'state': 'CANCELED'}]
executed = filter_by_state(operations) # По умолчанию ищет 'EXECUTED'
~~~
Сортировка по дате (sort_by_date)
Функция сортирует операции по полю date.

~~~
from src.processing import sort_by_date

sorted_ops = sort_by_date(operations) # По убыванию (новые -> старые)
sorted_ops_asc = sort_by_date(operations, reverse=False) # По возрастанию (старые -> новые)
~~~
## Вклад в проект
### Мы приветствуем ваш вклад! 
Пожалуйста, следуйте процессу GitFlow:

#### Создайте новую ветку от develop:
~~~
git checkout -b feature/ваша-фича
~~~
#### Внесите изменения и сделайте коммиты.
#### Отправьте изменения в ваш форк и создайте Pull Request в ветку develop.

## Лицензия
Проект распространяется под лицензией MIT.