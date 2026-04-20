"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""

from flask import Flask
import subprocess

app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    """
    Возвращает uptime системы в упорядоченном формате.
    """
    result = subprocess.run(
        ["uptime", "-p"],
        capture_output=True,
        text=True,
        check=True
    )

    uptime_value = result.stdout.split()

    if uptime_value.startswith("up "):
        uptime_value = uptime_value[3:]

    return f"Current uptime is {uptime_value}"


if __name__ == '__main__':
    app.run(debug=True)
