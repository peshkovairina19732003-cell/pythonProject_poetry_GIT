# tests/test_decorators.py

import logging  # <--- Импорт нужен для уровня ERROR
import os
import tempfile
import time  # <--- Задержка

import pytest

# Обязательный импорт
from src.decorators.logging import log


@pytest.fixture(scope="session")
def temp_log_file():
    """Временный файл для логов."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    yield temp_file.name
    # os.unlink(temp_file.name)


@pytest.fixture
def caplog_fixture():
    """Фикстура для перехвата логов в памяти."""

    import logging
    import logging.handlers
    from io import StringIO

    log_capture = StringIO()
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(log_capture)
    root_logger.addHandler(handler)
    yield log_capture
    root_logger.removeHandler(handler)


class TestLogDecorator:
    """Комплексные тесты для декоратора @log."""

    def test_log_to_file(self, temp_log_file):
        """Проверка логирования в файл."""

        @log(temp_log_file)
        def simple_add(a, b):
            return a + b

        result = simple_add(2, 3)
        assert result == 5

        with open(temp_log_file, 'r', encoding='UTF-8') as f:
            content = f.read()
            assert "START simple_add" in content
            assert "DONE simple_add" in content
            assert "Result: 5" in content
            assert "Time: " in content  # Проверка тайминга

    def test_log_to_console(self, caplog_fixture):
        """Проверка логирования в консоль."""

        @log()
        def greet(name: str):
            return f"Hello, {name}!"

        result = greet("Alice")
        assert result == "Hello, Alice!"  # Декоратор не искажает результат

        captured_logs = caplog_fixture.getvalue()
        assert "START greet" in captured_logs
        assert "DONE greet" in captured_logs
        assert "Result: Hello, Alice!" in captured_logs
        assert "Time: " in captured_logs  # Проверка тайминга

    def test_log_error_handling(self, caplog_fixture):
        """Проверка логирования ошибок."""

        @log()
        def fail_func(x):
            if x < 0:
                raise ValueError("Negative!")
            return x

        with pytest.raises(ValueError):
            fail_func(-1)

        captured_logs = caplog_fixture.getvalue()
        assert "START fail_func" in captured_logs
        assert "FAILURE fail_func" in captured_logs
        assert "Negative!" in captured_logs
        assert "Time: " in captured_logs  # Проверка тайминга

    def test_log_level_control(self, caplog_fixture):
        """Проверка управления уровнем логирования."""

        @log(level=logging.ERROR)
        def silent_pass():
            return "Silent"

        result = silent_pass()
        assert result == "Silent"

        captured_logs = caplog_fixture.getvalue()
        assert "Silent" not in captured_logs  # ERROR-level не захватывает INFO

    def test_parallel_usage(self):
        """Проверка параллельного использования декоратора."""

        # Используем УНИКАЛЬНЫЕ имена файлов
        unique_a_path = './logs/test_a_unique.log'
        unique_b_path = './logs/test_b_unique.log'

        @log(unique_a_path)
        def foo():
            return "Foo"

        @log(unique_b_path)
        def bar():
            return "Bar"

        foo_result = foo()
        bar_result = bar()

        assert foo_result == "Foo"
        assert bar_result == "Bar"

        # Ждем, пока ОС сбросит буферы
        time.sleep(0.1)

        # Проверяем, что файлы существуют
        assert os.path.isfile(unique_a_path)
        assert os.path.isfile(unique_b_path)

        # Читаем файлы, только если они есть
        if os.path.isfile(unique_a_path):
            with open(unique_a_path, 'r', encoding='UTF-8') as fa:
                a_content = fa.read()
                assert "foo" in a_content and "bar" not in a_content

        if os.path.isfile(unique_b_path):
            with open(unique_b_path, 'r', encoding='UTF-8') as fb:
                b_content = fb.read()
                assert "bar" in b_content and "foo" not in b_content

        # 🔸 Удаляем файлы сразу после теста
        if os.path.isfile(unique_a_path):
            os.remove(unique_a_path)

        if os.path.isfile(unique_b_path):
            os.remove(unique_b_path)
