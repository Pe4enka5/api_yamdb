import datetime

from django.core.validators import MaxValueValidator
from django.forms import ValidationError

from api_yamdb import settings


def max_value_current_year(value):
    return MaxValueValidator(
        datetime.date.today().year, 'Год не может быть больше текущего'
    )(value)


def validate_username(username):
    if username in settings.NOT_USERNAME:
        raise ValidationError('Использовать имя "me" запрещено')
    return username
