from http import HTTPStatus

from api.serializers import CommentSerializer, ReviewSerializer
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import response, viewsets
from reviews.models import Category, Comment, Genre, Review, Title

from .filtersets import TitleFilter
from .mixins import (AdminOrReadOnlyMixin, AuthorPermissionMixin, GetPostMixin,
                     PaginationMixin, SearchAndFilterMixin)
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleDetailSerializer, TitleSerializer)


class BaseCatGenreViewSet(
    AdminOrReadOnlyMixin,
    SearchAndFilterMixin,
    PaginationMixin,
    GetPostMixin,
    viewsets.ModelViewSet,
):
    """Абстрактный базовый вьюсет для вьюсетов простых моделей."""

    pass


class TitleViewSet(
    AdminOrReadOnlyMixin, PaginationMixin, viewsets.ModelViewSet
):
    """Возвращает список тайтлов, позволяет их добавлять и редактировать."""

    queryset = Title.objects.all().annotate(rating=Avg("reviews__score"))
    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )
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
        return (
            TitleDetailSerializer
            if self.action in ["retrieve"]
            else TitleSerializer
        )

    def create(self, request, *args, **kwargs):
        """Создает произведение и возвращает детализацию."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=HTTPStatus.CREATED)


class CategoryViewSet(BaseCatGenreViewSet):
    """Возвращает список категорий и позволяет их добавлять и редактировать."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseCatGenreViewSet):
    """Возвращает список жанров и позволяет их добавлять и редактировать."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с отзывами.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )

    def get_post_id(self):
        """Возвращает id произведения."""
        return self.kwargs.get("title_id")

    def perform_create(self, serializer):
        """Создает рецензию, указывая произведение с id, переданным в URL."""
        title_id = self.get_post_id()
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.get_post_id()
        return self.queryset.filter(title_id=title_id)


class CommentViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с комментариями.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )

    def get_post_id(self):
        """Возвращает id рецензии."""
        return self.kwargs.get("review_id")

    def perform_create(self, serializer):
        """Создает коммент, указывая рецензию с id, переданным в URL."""
        review_id = self.get_post_id()
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.get_post_id()
        return self.queryset.filter(review_id=review_id)
