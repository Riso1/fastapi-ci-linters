"""
В этом файле будут Celery-задачи
"""

from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "homework",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

# Основные настройки celery
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

# Чтобы celery видел задачи из этих файлов
celery_app.conf.imports = ("image", "mail")

# Периодические задачи для celery beat
celery_app.conf.beat_schedule = {
    "send-weekly-mailing": {
        "task": "mail.send_weekly_mailing",
        # Раз в неделю, в понедельник в 09:00
        "schedule": crontab(minute=0, hour=9, day_of_week=1),
    }
}

celery_app.set_default()
celery_app.set_current()
