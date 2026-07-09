# src/decorators/logging.py

import contextlib
import functools
import logging
import os
import time
from typing import Any, Callable, Optional, TypeVar

F = TypeVar('F', bound=Callable[..., Any])

def log(filename: Optional[str] = None, level: int = logging.INFO) -> Callable[[F], F]:
    """
    Декоратор для автоматического логирования функций.

    Args:
        filename (Optional[str]): Имя файла для логов. Если None — выводит в консоль.
        level (int): Уровень логирования (по умолчанию INFO).

    Returns:
        Callable: Обернутая функция.
    """

    class LogContext(contextlib.AbstractContextManager):
        """Контекст для надежного управления логгерами"""

        def __init__(self, logger: logging.Logger, handler: logging.Handler):
            self.logger = logger
            self.handler = handler

        def __enter__(self):
            self.logger.addHandler(self.handler)

        def __exit__(self, exc_type, exc_val, exc_tb):
            # Освобождаем хендлер
            self.logger.removeHandler(self.handler)
            self.handler.flush()
            self.handler.close()

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Создаем уникальный логгер для каждой функции
            logger = logging.getLogger(f"{func.__module__}.{func.__name__}")
            logger.setLevel(level)

            # Настройка логгера
            if filename:
                # Создаем папку, если её нет
                log_dir = os.path.dirname(filename)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir)

                handler = logging.FileHandler(filename, mode='a', encoding='utf-8')
            else:
                handler = logging.StreamHandler()

            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)

            # Блокируем управление логером
            with LogContext(logger, handler):
                start_time = time.time()
                try:
                    logger.info(f"START {func.__name__}")
                    result = func(*args, **kwargs)
                    duration = round(time.time() - start_time, 3)
                    logger.info(f"DONE {func.__name__} | Result: {result} | Time: {duration:.3f}s")
                    return result
                except Exception as e:
                    duration = round(time.time() - start_time, 3)
                    logger.error(
                        f"FAILURE {func.__name__} "
                        f"| Error: {repr(e)} "
                        f"| Input args: {args}, kwargs: {kwargs} "
                        f"| Time: {duration:.3f}s",
                        exc_info=True
                    )
                    raise

        return wrapper

    return decorator
