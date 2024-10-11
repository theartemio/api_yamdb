from api.serializers import CommentSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, response, serializers, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Category, Comment, Genre, Review, Title
from users.permissions import IsAdminOrReadonly, IsAuthOrReadOnly

from .filtersets import TitleFilter
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleDetailSerializer, TitleSerializer)


class PaginationMixin:
    """Миксин для настройки пагинации."""
    pagination_class = LimitOffsetPagination


class AuthorPermissionMixin:
    """Миксин для проверки доступа автора и модера."""
    permission_classes = (IsAuthOrReadOnly,)


class AdminOrReadOnlyMixin:
    """Миксин для проверки админства."""
    permission_classes = (IsAdminOrReadonly, )


class GetPostMixin:
    """Миксин для ограничения методов."""
    http_method_names = ['get', 'post', 'delete']

    def retrieve(self, request, *args, **kwargs):
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SearchAndFilterMixin:
    """Миксин для поиска по имени и фильтрации по слагу."""
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(AdminOrReadOnlyMixin,
                   PaginationMixin,
                   viewsets.ModelViewSet):
    """Возвращает список тайтлов, позволяет их добавлять и редактировать."""

    queryset = Title.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def list(self, request, *args, **kwargs):
        """Выдача объектов списом по нужной форме."""
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TitleDetailSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TitleDetailSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия."""
        return (TitleDetailSerializer
                if self.action in ['retrieve']
                else TitleSerializer)

    def create(self, request, *args, **kwargs):
        """Создает произведение и возвращает детализацию."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.save()
        return response.Response(TitleDetailSerializer(title).data, status=201)


class CategoryViewSet(AdminOrReadOnlyMixin,
                      SearchAndFilterMixin,
                      PaginationMixin,
                      GetPostMixin,
                      viewsets.ModelViewSet):
    """Возвращает список категорий и позволяет их добавлять и редактировать."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(AdminOrReadOnlyMixin,
                   SearchAndFilterMixin,
                   PaginationMixin,
                   GetPostMixin,
                   viewsets.ModelViewSet):
    """Возвращает список жанров и позволяет их добавлять и редактировать."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с отзывами.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_post_id(self):
        """Возвращает id произведения."""
        return self.kwargs.get("title_id")

    def perform_create(self, serializer):
        """Создает рецензию, указывая произведение с id, переданным в URL."""
        title_id = self.get_post_id()
        title = get_object_or_404(Title, pk=title_id)

        if Review.objects.filter(author=self.request.user,
                                 title=title).exists():
            error_message = ("""У вас уже была рецензия на это произведение.
                             Вы можете удалить ее и написать новую или
                             внести изменения.""")
            raise serializers.ValidationError({"detail": error_message})

        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return self.queryset.filter(title_id=title_id)


class CommentViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с комментариями.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_post_id(self):
        """Возвращает id рецензии."""
        return self.kwargs.get("review_id")

    def perform_create(self, serializer):
        """Создает коммент, указывая рецензию с id, переданным в URL."""
        review_id = self.get_post_id()
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return self.queryset.filter(review_id=review_id)
