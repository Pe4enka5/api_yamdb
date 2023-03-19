from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (Category, Comment,
                            Genre, Review, Title)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        avg_rating = (
            Review.objects.filter(title_id=obj.id).
            aggregate(Avg('rating'))['avg__rating']
        )
        if avg_rating is None:
            return None
        else:
            return round(avg_rating, 0)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        fields = (
            'id',
            'author',
            'text',
            'pub_date',
            'rating',
            'title'
        )
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Вы уже оставляли отзыв на данное произведение'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    review = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        fields = (
            'author',
            'text',
            'created',
            'review'
        )
        model = Comment
