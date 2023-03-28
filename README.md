# Проект YaMDb

### Описание
Проект YaMDb собирает отзывы пользователей на произведения.

### Технологии
Python 3.7,
Django 2.2.19
Django Rest Framework 3.12.4
Simple JWT
### Как запустить проект:
- Клонировать репозиторий и перейти в него в командной строке:

```git clone https://github.com:Pe4enka5/api_yamdb.git```

```cd api_yamdb```

- Cоздать и активировать виртуальное окружение:

```python -m venv venv```

```source venv/bin/activate```

```python -m pip install --upgrade pip```

- Установить зависимости из файла requirements.txt:

```pip install -r requirements.txt```

- Выполнить миграции:

```python manage.py migrate```

- Заполнить базу данных тестовым контентом:

```python manage.py importcsv```

- Запустить проект:

```python manage.py runserver```

- Посмотреть документацию при запущенном сервере (см. выше):

```[Ссылка на документацию](http://127.0.0.1:8000/redoc/)```

### Автор:
- Печерица Андрей - [Github_Pe4enka5](https://github.com/Pe4enka5)
- Мальшаков Александр - [Github_morongod](https://github.com/morongod)
- Михайлов Андрей - [Github_Andew-063](https://github.com/Andew-063)
