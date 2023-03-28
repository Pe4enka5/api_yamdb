from rest_framework import serializers

from api_yamdb.settings import (
    CONFIRMATION_CODE_MAX_LENGTH, EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
)
from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import validate_username


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
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True
    )
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User

    def validate_username(self, value):
        return validate_username(value)


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)
    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)

    def validate_username(self, value):
        return validate_username(value)


class TokenUserSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH, required=True
    )
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_MAX_LENGTH, required=True
    )

    def validate_username(self, value):
        return validate_username(value)


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
        request = self.context['request']
        title_id = self.context.get('view').kwargs.get('title_id')
        if (
            request.method == 'POST'
            and Review.objects.filter(
                title=title_id,
                author=request.user
            ).exists()
        ):
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
