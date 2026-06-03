"""
Здесь происходит логика обработки изображения
"""

from typing import Optional

from PIL import Image, ImageFilter

from celery import shared_task

from mail import send_email_task


def blur_image(src_filename: str, dst_filename: Optional[str] = None):
    """
    Функция принимает на вход имя входного и выходного файлов.
    Применяет размытие по Гауссу со значением 5.
    """
    if not dst_filename:
        dst_filename = f'blur_{src_filename}'

    with Image.open(src_filename) as img:
        img.load()
        new_img = img.filter(ImageFilter.GaussianBlur(5))
        new_img.save(dst_filename)


@shared_task(name="image.process_image")
def process_image(src_filename: str, dst_filename: str, order_id: str, receiver: str):
    """
    Задача для celery.
    Размывает изображение и потом отправляет его на почту.
    """
    blur_image(src_filename, dst_filename)
    send_email_task.delay(order_id, receiver, dst_filename)
    return dst_filename