from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets

from api.filtres import TitleFilter
from api.mixins import ListGreateDeleteViewSet
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, TitleCreateSerializer)
from reviews.models import Category, Genre, Title


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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer
