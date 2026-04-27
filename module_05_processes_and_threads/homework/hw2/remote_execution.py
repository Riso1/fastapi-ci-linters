"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""

import subprocess
import sys

from flask import Flask, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, InputRequired

app = Flask(__name__)
app.config["WTF_CSRF_ENABLED"] = False

class CodeForm(FlaskForm):
    code = StringField(validators=[DataRequired(message="Введите код")])
    timeout = IntegerField(
        validators=[
            InputRequired(message="Введите тайм-аут"),
            NumberRange(min=1, max=30, message="Тайм-аут должен быть от 1 до 30 секунд")
        ]
    )


def run_python_code_in_subproccess(code: str, timeout: int):
    process = subprocess.Popen(
        ["prlimit", "--nproc=1:1", sys.executable, "-c", code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        stdout, stderr = process.communicate(timeout=timeout)
        return {
            "status": "ok",
            "stdout": stdout,
            "stderr": stderr,
            "returncode": process.returncode
        }

    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        return {
            "status": "timeout",
            "message": "Execution timed out",
            "stdout": stdout,
            "stderr": stderr
        }


@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()

    if not form.validate_on_submit():
        return jsonify({
            "status": "error",
            "errors": form.errors
        }), 400

    result = run_python_code_in_subproccess(
        code=form.code.data,
        timeout=form.timeout.data
    )

    if result["status"] == "timeout":
        return jsonify(result), 408

    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=True)
