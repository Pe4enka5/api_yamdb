from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(max_length=256, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год')
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenres',
        verbose_name='Жанр',
        related_name='genre'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='category'

    )

    def __str__(self):
        return self.name


class TitleGenres(models.Model):
    title = models.ForeignKey(Title, null=True, on_delete=models.SET_NULL)
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL)
