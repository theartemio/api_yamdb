from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Category, Genre, Title

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class SearchMixin:
    """Миксин для поиска по названию."""
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class PaginationMixin:
    """Миксин для настройки пагинации."""
    pagination_class = LimitOffsetPagination


class GetPostMixin:
    """Миксин для ограничения методов."""
    http_method_names = ['get', 'post']


class TitleViewSet(PaginationMixin, viewsets.ModelViewSet):
    """Возвращает список тайтлов, позволяет их добавлять и редактировать."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # тут будут фильтры
    # filterset_fields = ('category', 'genre', 'name', 'year')


class CategoryViewSet(SearchMixin,
                      PaginationMixin,
                      GetPostMixin,
                      viewsets.ModelViewSet):
    """Возвращает список категорий и позволяет их добавлять и редактировать."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(SearchMixin,
                   PaginationMixin,
                   GetPostMixin,
                   viewsets.ModelViewSet):
    """Возвращает список жанров и позволяет их добавлять и редактировать."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
