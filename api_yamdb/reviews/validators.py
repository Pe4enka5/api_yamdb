from django.forms import ValidationError

from api_yamdb import settings


def validate_username(username):
    if username in settings.NOT_USERNAME:
        raise ValidationError('Использовать имя "me" запрещено')
    return username
