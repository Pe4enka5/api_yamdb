from django.contrib import admin
from reviews.models import (Category, Comment, Genre, Review, Title,
                            TitleGenres, User)


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(TitleGenres)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(User)


class UserAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )
    empty_value_display = 'значение отсутствует'
    list_editable = ('role',)
    list_filter = ('username',)
    search_fields = ('username', 'role')
