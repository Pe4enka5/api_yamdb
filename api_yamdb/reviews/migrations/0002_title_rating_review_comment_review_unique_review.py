# Generated by Django 4.1.7 on 2023-03-19 05:20

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.FloatField(blank=True, null=True, verbose_name='Рейтинг'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Отзыв')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Рейтинг')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to=settings.AUTH_USER_MODEL, verbose_name='Юзер')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review', to='reviews.title', verbose_name='Произведение')),
            ],
            options={
                'ordering': ['pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Юзер')),
                ('review', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.review', verbose_name='Отзыв')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique_review'),
        ),
    ]
