"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import ValidationError


def number_length(min: int, max: int, message: Optional[str] = None):
    if min < 0 or max < 0:
        raise ValueError("min и max не могут быть отрицательными")
    if min > max:
        raise ValueError("min не может быть больше max")

    def _number_length(form: FlaskForm, field: Field):
        if field.data is None:
            return

        value_length = len(str(abs(field.data)))

        if value_length < min or value_length > max:
            raise ValidationError(
                message or f"Длина числа может быть от {min} до {max} символов."
            )

    return _number_length


class NumberLength:
    def __init__(self, min: int, max: int, message: Optional[str] = None):
        if min < 0 or max < 0:
            raise ValueError("min и max не могут быть отрицательными")
        if min > max:
            raise ValueError("min не может быть больше max")

        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        if field.data is None:
            return

        value_length = len(str(abs(field.data)))

        if value_length < self.min or value_length > self.max:
            raise ValidationError(
                self.message
                or f"Длина числа должна быть от {self.min} до {self.max} символов."
            )
