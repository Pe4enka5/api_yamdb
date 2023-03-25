import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from reviews.models import (Category, Comment, Genre, Review, Title,
                            TitleGenres, User)


def process_file(name: str):
    return csv.reader(open(os.path.join(settings.BASE_DIR,
                                        'static/data/',
                                        name), 'r', encoding='utf-8'),
                      delimiter=',')


class Command(BaseCommand):

    def handle(self, *args, **options):

        # парсер юзеров
        csv = process_file('users.csv')
        next(csv, None)
        for row in csv:
            obj, created = User.objects.get_or_create(id=row[0],
                                                      username=row[1],
                                                      email=row[2],
                                                      role=row[3],
                                                      bio=row[4],
                                                      first_name=row[5],
                                                      last_name=row[6])
        print('парсер пользователей прошел успешно')

        # парсер категорий
        csv = process_file('category.csv')
        next(csv, None)
        for row in csv:
            obj, created = Category.objects.get_or_create(id=row[0],
                                                          name=row[1],
                                                          slug=row[2])
        print('парсер категорий прошел успешно')

        # парсер жанров
        csv = process_file('genre.csv')
        next(csv, None)
        for row in csv:
            obj, created = Genre.objects.get_or_create(id=row[0],
                                                       name=row[1],
                                                       slug=row[2])
        print('парсер жанров прошел успешно')

        # парсер титлов
        csv = process_file('titles.csv')
        next(csv, None)
        for row in csv:
            obj, created = (Title
                            .objects
                            .get_or_create(id=row[0],
                                           name=row[1],
                                           year=row[2],
                                           category=get_object_or_404(Category,
                                                                      id=row[3]
                                                                      )))
        print('парсер титлов прошел успешно')

        # пасрер жанро-титлов
        csv = process_file('genre_title.csv')
        next(csv, None)
        for row in csv:
            obj, created = (TitleGenres
                            .objects
                            .get_or_create(id=row[0],
                                           title=get_object_or_404(Title,
                                                                   id=row[1]),
                                           genre=get_object_or_404(Genre,
                                                                   id=row[2])))
        print('зависимости между жанрами и произведениями установлены')

        # парсер отзывов
        csv = process_file('review.csv')
        next(csv, None)
        for row in csv:
            obj, created = (Review
                            .objects
                            .get_or_create(id=row[0],
                                           title=get_object_or_404(Title,
                                                                   id=row[1]),
                                           text=row[2],
                                           author=get_object_or_404(User,
                                                                    id=row[3]),
                                           score=row[4],
                                           pub_date=row[5]))
        print('парсер отзывов завершен')

        # парсер коментов
        csv = process_file('comments.csv')
        next(csv, None)
        for row in csv:
            obj, created = (Comment
                            .objects
                            .get_or_create(id=row[0],
                                           review=get_object_or_404(Review,
                                                                    id=row[1]),
                                           text=row[2],
                                           author=get_object_or_404(User,
                                                                    id=row[3]),
                                           pub_date=row[4]))
        print('комментарии установлены')
