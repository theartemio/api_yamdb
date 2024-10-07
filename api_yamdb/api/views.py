from typing import Optional, Type
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Model
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.permissions import IsAuthorOrStaff
from api.serializers import CommentSerializer, ReviewSerializer
from reviews.models import Category, Comment, Genre, Review, Title

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class SearchMixin:
    """Миксин для поиска по названию."""
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class PaginationMixin:
    """Миксин для настройки пагинации."""
    pagination_class = LimitOffsetPagination


class SlugLookupMixin:
    """Миксин для доступа по URL со слагом."""
    lookup_field = 'slug'


# Я не уверен, что это нужно, но в Redoc не прописаны методы patch для
# категорий и жанров, поэтому пусть пока будет на случай,
# если тесты это проверяют.
class GetPostMixin:
    """Миксин для ограничения методов."""
    http_method_names = ['get', 'post', 'delete']

class AuthMixin:
    """Миксин для проверки авторства."""
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrStaff]


class NestedViewSetMixin:
    """
    Миксин для получения id вложенного объекта и выполнения метода create.
    """
    parent_lookup_field: Optional[str] = None
    parent_model: Optional[Type[Model]] = None
    related_field: Optional[str] = None

    def get_parent_object(self):
        """
        Получает родительский объект по переданному идентификатору.
        """
        parent_id = self.kwargs.get(self.parent_lookup_field)
        return get_object_or_404(self.parent_model, pk=parent_id)

    def perform_create(self, serializer):
        """
        Создает объект, передавая в сериализатор родительский объект.
        """
        parent_object = self.get_parent_object()
        serializer.save(**{self.related_field: parent_object})

    def get_queryset(self):
        parent_id = self.kwargs.get(self.parent_lookup_field)
        return self.queryset.filter(**{f'{self.related_field}_id': parent_id})


class TitleViewSet(PaginationMixin, viewsets.ModelViewSet):
    """Возвращает список тайтлов, позволяет их добавлять и редактировать."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')


class CategoryViewSet(SearchMixin,
                      PaginationMixin,
                      GetPostMixin,
                      SlugLookupMixin,
                      viewsets.ModelViewSet):
    """Возвращает список категорий и позволяет их добавлять и редактировать."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(SearchMixin,
                   PaginationMixin,
                   GetPostMixin,
                   SlugLookupMixin,
                   viewsets.ModelViewSet):
    """Возвращает список жанров и позволяет их добавлять и редактировать."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(NestedViewSetMixin, viewsets.ModelViewSet):  #  Add AuthMixin
    """
    ViewSet для работы с отзывами.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    parent_lookup_field = 'title_id'
    parent_model = Title
    related_field = 'title'


class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с комментариями.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    parent_lookup_field = 'review_id'
    parent_model = Review
    related_field = 'review'
