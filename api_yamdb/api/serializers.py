from rest_framework import serializers

from reviews.models import Category, Genre, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username',)


class TokenUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
