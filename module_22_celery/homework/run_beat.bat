@echo off
celery -A celery_app.celery_app beat --loglevel=info