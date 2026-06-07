import json
import re
from typing import Callable, Optional


class WSGIApp:
    """
    Простое самописное WSGI-приложение.
    Поддерживает регистрацию маршрутов через декоратор.
    """

    def __init__(self) -> None:
        self.routes: list[tuple[str, Callable]] = []

    def route(self, pattern: str) -> Callable:
        """
        Декоратор для регистрации маршрута.
        """

        def decorator(func: Callable) -> Callable:
            self.routes.append((pattern, func))
            return func

        return decorator

    def _match_route(self, path: str) -> tuple[Optional[Callable], dict]:
        """
        Ищет подходящий маршрут и возвращает функцию и параметры пути.
        Например:
        /hello/user -> pattern /hello/<name>
        """
        for pattern, func in self.routes:
            regex_pattern = "^" + re.sub(r"<([^>]+)>", r"(?P<\1>[^/]+)", pattern) + "$"
            match = re.match(regex_pattern, path)
            if match:
                return func, match.groupdict()
        return None, {}

    def __call__(self, environ: dict, start_response: Callable) -> list[bytes]:
        """
        Точка входа WSGI-приложения.
        """
        path = environ.get("REQUEST_URI") or environ.get("PATH_INFO", "/")

        view_func, params = self._match_route(path)

        if view_func is None:
            status = "404 Not Found"
            response_body = json.dumps(
                {"error": "Страница не найдена"},
                ensure_ascii=False,
                indent=4,
            )
        else:
            status = "200 OK"
            response_body = view_func(**params)

        response_bytes = response_body.encode("utf-8")
        headers = [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(response_bytes))),
        ]

        start_response(status, headers)
        return [response_bytes]


app = WSGIApp()


@app.route("/hello")
def say_hello() -> str:
    """
    Обработчик для /hello
    """
    return json.dumps(
        {"response": "Hello, world!"},
        ensure_ascii=False,
        indent=4,
    )


@app.route("/hello/<name>")
def say_hello_with_name(name: str) -> str:
    """
    Обработчик для /hello/<name>
    """
    return json.dumps(
        {"response": f"Hello, {name}!"},
        ensure_ascii=False,
        indent=4,
    )
