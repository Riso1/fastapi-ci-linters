"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""

import sys
import traceback
from types import TracebackType
from typing import Type, Literal, IO


class Redirect:
    def __init__(self, *, stdout: IO = None, stderr: IO = None) -> None:
        self.new_stdout = stdout
        self.new_stderr = stderr
        self.old_stdout = None
        self.old_stderr = None

    def __enter__(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

        if self.new_stdout is not None:
            sys.stdout = self.new_stdout

        if self.new_stderr is not None:
            sys.stderr = self.new_stderr

        return self

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        if exc_type is not None and self.new_stderr is not None:
            self.new_stderr.write(
                "".join(traceback.format_exception(exc_type, exc_val, exc_tb))
            )

        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

        if exc_type is not None and self.new_stderr is not None:
            return True

        return None
