from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    class Role(models.TextChoices):
        'Роль',
        USER = 'user', ('user'),
        MODERATOR = 'moderator', ('moderator'),
        ADMIN = 'admin', ('admin')

    role = models.CharField(
        max_length=15,
        choices=Role.choices,
        default=Role.USER,
    )
