import pytest
from src.decorators import log


def test_log_to_console(capsys):
    """Проверка вывода лога в консоль."""

    @log()  # Без аргумента filename -> console
    def add(a: int, b: int) -> int:
        return a + b

    assert add(2, 3) == 5

    captured = capsys.readouterr()
    out = captured.out

    assert "add ok" in out
    assert "(2, 3)" in out or "Args: (2, 3)" in out


def test_log_to_file(tmp_path):
    """Проверка записи лога в файл."""
    log_file = tmp_path / "test_log.log"

    @log(filename=str(log_file))
    def divide(a: float, b: float) -> float:
        return a / b

    res = divide(10, 2)
    assert res == 5.0

    content = log_file.read_text()
    assert "divide ok" in content
    assert "(10, 2)" in content or "Args: (10, 2)" in content


def test_log_error_handling(caplog):
    """Проверка логирования ошибок."""

    @log()
    def fail_func(x):
        raise ValueError("Test exception")

    with pytest.raises(ValueError):
        fail_func(10)

    # Проверяем, что ошибка залогирована
    errors = [rec for rec in caplog.records if rec.levelname == 'ERROR']
    assert len(errors) == 1
    assert "fail_func error: ValueError" in errors[0].message
    assert "Inputs: args=(10,)" in errors[0].message
