"""
В этом файле будет ваше Flask-приложение
"""

import os
import uuid

from flask import Flask, jsonify, request
from celery.result import GroupResult
from celery import group

from celery_app import celery_app
from image import process_image
from mail import subscribe_email, unsubscribe_email

app = Flask(__name__)

UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


@app.route("/blur", methods=["POST"])
def blur():
    """
    Принимает картинки и почту.
    Ставит задачи в очередь на обработку.
    """
    email = request.form.get("email")
    images = request.files.getlist("images")

    if not email:
        return jsonify({"error": "Не указана почта"}), 400

    if not images:
        return jsonify({"error": "Не переданы изображения"}), 400

    order_id = str(uuid.uuid4())
    tasks = []

    for image in images:
        ext = os.path.splitext(image.filename)[1] or ".jpg"
        src_filename = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{ext}")
        dst_filename = os.path.join(PROCESSED_DIR, f"blur_{uuid.uuid4()}{ext}")

        image.save(src_filename)

        tasks.append(
            process_image.s(src_filename, dst_filename, order_id, email)
        )

    job = group(tasks, app=celery_app).apply_async()
    job.save()

    return jsonify({
        "order_id": order_id,
        "group_id": job.id,
    }), 202


@app.route("/status/<task_id>", methods=["GET"])
def status(task_id: str):
    """
    Возвращает прогресс группы задач.
    """
    result = GroupResult.restore(task_id, app=celery_app)

    if result is None:
        return jsonify({"error": "Группа задач не найдена"}), 404

    total = len(result.results)
    done = sum(1 for item in result.results if item.ready())

    if result.ready():
        status_text = "processed"
    else:
        status_text = "processing"

    return jsonify({
        "group_id": task_id,
        "status": status_text,
        "done": done,
        "total": total,
    }), 200


@app.route("/subscribe", methods=["POST"])
def subscribe():
    """
    Подписка на еженедельную рассылку.
    """
    data = request.get_json(silent=True) or {}
    email = data.get("email")

    if not email:
        return jsonify({"error": "Не указана почта"}), 400

    subscribe_email(email)
    return jsonify({"message": "Подписка оформлена"}), 200


@app.route("/unsubscribe", methods=["POST"])
def unsubscribe():
    """
    Отписка от еженедельной рассылки.
    """
    data = request.get_json(silent=True) or {}
    email = data.get("email")

    if not email:
        return jsonify({"error": "Не указана почта"}), 400

    unsubscribe_email(email)
    return jsonify({"message": "Подписка отменена"}), 200


if __name__ == "__main__":
    app.run(debug=True)