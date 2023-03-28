from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.mixins import UsernameValidateMixin
from api_yamdb.settings import (
    CONFIRMATION_CODE_MAX_LENGTH, EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
)
from reviews.models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = fields
        model = Title


class CustomUserSerializer(serializers.ModelSerializer, UsernameValidateMixin):

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class UserRegisterSerializer(serializers.Serializer, UsernameValidateMixin):
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)
    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)


class TokenUserSerializer(serializers.Serializer, UsernameValidateMixin):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH, required=True
    )
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_MAX_LENGTH, required=True
    )


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if Review.objects.filter(
            author=self.context['request'].user,
            title=get_object_or_404(
                Title,
                id=self.context['view'].kwargs.get('title_id')
            )
        ).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв'
            )
        return data

    class Meta:
        fields = (
            'id',
            'author',
            'text',
            'pub_date',
            'score',
        )
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = (
            'id',
            'author',
            'text',
            'pub_date',
        )
        model = Comment
