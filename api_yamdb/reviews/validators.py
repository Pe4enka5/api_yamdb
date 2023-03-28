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
        username_list = re.findall(r'.', username)
        forbidden_simvols = []
        for i in username_list:
            a = re.findall(r'^[\w.@+-]+\Z', i)
            if a == []:
                if i not in forbidden_simvols:
                    forbidden_simvols.append(i)
        result = ', '.join(forbidden_simvols)
        raise ValidationError(
            'Имя пользователя содержит недопустимые символы: '
            f'{result}'
        )
    return username
