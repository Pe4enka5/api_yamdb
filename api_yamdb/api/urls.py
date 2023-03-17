from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CustomUserViewSet, GenreViewSet,
                       RegisterUserViewSet, TitleViewSet, TokenUserViewSet)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', CustomUserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenUserViewSet.as_view(), name='token_obtain_pair'),
    path('v1/auth/signup/', RegisterUserViewSet.as_view(), name='register_user'),
]
