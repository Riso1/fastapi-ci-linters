import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import shared_task

from config import SMTP_HOST, SMTP_PORT, SMTP_PASSWORD, SMTP_USER

SUBSCRIBERS_FILE = "subscribers.txt"


def send_email(order_id: str, receiver: str, filename: str):
    """
    Отправляет пользователю `receiver` письмо по заказу `order_id` с приложенным файлом `filename`

    Вы можете изменить логику работы данной функции
    """
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        email = MIMEMultipart()
        email['Subject'] = f'Изображения. Заказ №{order_id}'
        email['From'] = SMTP_USER
        email['To'] = receiver

        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(filename)}'
        )
        email.attach(part)
        text = email.as_string()

        server.sendmail(SMTP_USER, receiver, text)


def get_subscribers() -> set[str]:
    """
    Читаем список подписчиков из файла.
    """
    if not os.path.exists(SUBSCRIBERS_FILE):
        return set()

    with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as file:
        return {line.strip() for line in file if line.strip()}


def save_subscribers(subscribers: set[str]):
    """
    Перезаписываем файл подписчиков.
    """
    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as file:
        for email in sorted(subscribers):
            file.write(email + "\n")


def subscribe_email(email: str):
    """
    Добавляем почту в список подписчиков.
    """
    subscribers = get_subscribers()
    subscribers.add(email)
    save_subscribers(subscribers)


def unsubscribe_email(email: str):
    """
    Удаляем почту из списка подписчиков.
    """
    subscribers = get_subscribers()
    subscribers.discard(email)
    save_subscribers(subscribers)


@shared_task(name="mail.send_email_task")
def send_email_task(order_id: str, receiver: str, filename: str):
    """
    Обертка над отправкой письма для celery.
    """
    send_email(order_id, receiver, filename)


@shared_task(name="mail.send_weekly_mailing")
def send_weekly_mailing():
    """
    Еженедельная рассылка.
    Здесь отправляем простое письмо о сервисе всем подписанным пользователям.
    """
    subscribers = get_subscribers()

    if not subscribers:
        return "Нет подписчиков"

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        for receiver in subscribers:
            email = MIMEMultipart()
            email["Subject"] = "Новости сервиса обработки изображений"
            email["From"] = SMTP_USER
            email["To"] = receiver
            email.attach(MIMEText("Спасибо, что пользуетесь сервисом обработки изображений!", "plain", "utf-8"))

            text = email.as_string()
            server.sendmail(SMTP_USER, receiver, text)

    return f"Отправлено писем: {len(subscribers)}"