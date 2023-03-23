from django.contrib import admin

from reviews.models import Category, Comment, Genre, Title, TitleGenres, Review

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(TitleGenres)
admin.site.register(Comment)
admin.site.register(Review)
