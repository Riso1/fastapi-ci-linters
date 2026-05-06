import json
from flask import Flask, request


app = Flask(__name__)

received_logs = []

@app.route('/log', methods=['POST'])
def log():
    """
    Записываем полученные логи которые пришли к нам на сервер
    return: текстовое сообщение об успешной записи, статус код успешной работы

    """
    log_record = request.form.to_dict()

    if log_record:
        received_logs.append(log_record)

    return "Log record saved", 200


@app.route('/logs', methods=['GET'])
def logs():
    """
    Рендерим список полученных логов
    return: список логов обернутый в тег HTML <pre></pre>
    """
    return f"<pre>{json.dumps(received_logs, indent=4, ensure_ascii=False)}</pre>", 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)