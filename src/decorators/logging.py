import functools
import logging
import sys
from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
from typing import Any, Callable, Dict, Iterator, List, Optional, TypeVar, cast

F = TypeVar('F', bound=Callable[..., Any])
R = TypeVar('R')


def log(filename: Optional[str] = None) -> Callable[[F], F]:
    """
    Декоратор для логирования вызовов функций.

    Если указан filename, пишет в файл. Иначе выводит в консоль.
    Логирует время выполнения, аргументы и результат/ошибку.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__

            # Используем StringIO как буфер для перехвата текста
            log_stream = StringIO()

            if filename:
                handler = logging.FileHandler(filename, encoding="utf-8")
            else:
                # ВАЖНО: Указываем stream=sys.stdout, чтобы capsys мог это поймать
                handler = logging.StreamHandler(stream=sys.stdout)

            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)

            logger = logging.getLogger(func_name)
            # Чистим хэндлеры перед добавлением нового, чтобы избежать дублирования при переиспользовании декоратора
            logger.handlers.clear()
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

            start_time = datetime.now()
            try:
                result = func(*args, **kwargs)
                duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

                msg_success = (
                    f"{func_name} ok | Duration: {duration_ms}ms | "
                    f"Args: {args}, Kwargs: {kwargs}"
                )
                logger.info(msg_success)
                return result
            except Exception as e:
                err_msg = (
                    f"{func_name} error: {type(e).__name__}. "
                    f"Inputs: args={args}, kwargs={kwargs}. Error: {e}"
                )
                logger.error(err_msg)
                raise
            finally:
                # Обязательно удаляем обработчик!
                logger.removeHandler(handler)
                handler.close()

        return cast(F, wrapper)

    return decorator
