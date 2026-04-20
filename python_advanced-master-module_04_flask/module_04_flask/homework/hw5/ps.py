"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""
import subprocess

from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    """
    Принимает аргументы команды ps через query-параметры arg
    и возвращает результат выполнения команды.
    """
    args = request.args.getlist("arg")

    result = subprocess.run(
        ["ps", *args],
        capture_output=True,
        text=True,
        check=True
    )
    return f"<pre>{escape(result.stdout)}</pre>"


if __name__ == "__main__":
    app.run(debug=True)
