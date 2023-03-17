from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import (CategorySerializer, CustomUserSerializer,
                             GenreSerializer, TitleSerializer,
                             TokenUserSerializer, UserRegisterSerializer)
from reviews.models import Category, Genre, Title
from users.models import User


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class RegisterUserViewSet(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            f'confirmation_code для {user.username}',
            f'{confirmation_code}',
            '89681115653@mail.ru',
            [f'{user.email}'],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenUserViewSet(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = TokenUserSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = TokenUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)
        token = AccessToken.for_user(user)
        return Response(str(token), status=status.HTTP_200_OK)
