import datetime
import re

from django.forms import ValidationError

from api_yamdb.settings import NOT_USERNAME


def max_value_current_year(value):
    year = datetime.date.today().year
    if value > year:
        raise ValidationError(f'Год произведения - "{value}" не может быть '
                              f'больше текущего года - "{year}"')
    return value


def validate_username(username):
    if username in NOT_USERNAME:
        raise ValidationError(f'Использовать имя "{username}" запрещено')

    result = re.sub(r'[\w.@+-]+', '', username)
    if result:
        raise ValidationError(
            'Имя пользователя содержит недопустимые символы: '
            f'{result}'
        )
    return username
