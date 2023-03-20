from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import (CategorySerializer, CommentSerializer, CustomUserSerializer,
                             GenreSerializer, ReviewSerializer, TitleSerializer, TitleCreateSerializer, 
                             TokenUserSerializer, UserRegisterSerializer)
from api.permissions import IsOwnerOrReadOnly
from reviews.models import Category, Genre, Review, Title
from api.filtres import TitleFilter
from api.mixins import ListGreateDeleteViewSet
from reviews.models import Category, Genre, Title
from users.models import User



class CategoryViewSet(ListGreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(
            name=self.request.data['name'], slug=self.request.data['slug']
        )

    def perform_destroy(self, serializer):
        serializer = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        serializer.delete()


class GenreViewSet(ListGreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    search_fields = ('name',)
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(
            name=self.request.data['name'], slug=self.request.data['slug']
        )

    def perform_destroy(self, serializer):
        serializer = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        serializer.delete()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.review.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title=title,
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        serializer.save(
            author=self.request.user,
            review=review
        )

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