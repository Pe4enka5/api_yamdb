import datetime
import re

from django.core.validators import MaxValueValidator
from django.forms import ValidationError

from api_yamdb.settings import NOT_USERNAME


def max_value_current_year(value):
    return MaxValueValidator(
        datetime.date.today().year, 'Год не может быть больше текущего'
    )(value)


def validate_username(username):
    if username in NOT_USERNAME:
        raise ValidationError(f'Использовать имя "{username}" запрещено')
    if not re.match(r'^[\w.@+-]+\Z', username):
        raise ValidationError('Имя пользователя содержит недопустимый символ')
    return username
