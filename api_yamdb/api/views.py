from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from rest_framework import serializers
from rest_framework import response

from api.serializers import CommentSerializer, ReviewSerializer
from reviews.models import Category, Comment, Genre, Review, Title
from users.permissions import IsAdminOrReadonly, IsAuthOrReadOnly

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, TitleDetailSerializer

from rest_framework import status
from rest_framework import response


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


class GetPostMixin:
    """Миксин для ограничения методов."""
    http_method_names = ['get', 'post', 'delete']


class AuthorPermissionMixin:
    """Миксин для проверки доступа автора и модера."""
    permission_classes = (IsAuthOrReadOnly,)


class AdminOrReadOnlyMixin:
    """Миксин для проверки админства."""
    permission_classes = (IsAdminOrReadonly, )


# Вьюсет, который не выдает ошибок KeyError: 'year'
# но выдает ошибки с категорией
'''
class TitleViewSet(AdminOrReadOnlyMixin,
                   PaginationMixin, viewsets.ModelViewSet):
    """Возвращает список тайтлов, позволяет их добавлять и редактировать."""
    # queryset = Title.objects.select_related('category').all()
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    http_method_names = ['get', 'post', 'patch', 'delete']
'''

# Вьюсет, который выдает ошибки KeyError, но вроде как пофиксена категория
class TitleViewSet(AdminOrReadOnlyMixin, PaginationMixin, viewsets.ModelViewSet):
    """Возвращает список тайтлов, позволяет их добавлять и редактировать."""

    queryset = Title.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def list(self, request, *args, **kwargs):
        """Выдача объектов списом по нужной форме."""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TitleDetailSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TitleDetailSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия."""
        return TitleDetailSerializer if self.action in ['retrieve', 'list'] else TitleSerializer

    def create(self, request, *args, **kwargs):
        """Создает произведение и возвращает детализацию."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.save()
        return response.Response(TitleDetailSerializer(title).data, status=201)


class CategoryViewSet(AdminOrReadOnlyMixin,
                      SearchMixin,
                      PaginationMixin,
                      GetPostMixin,
                      SlugLookupMixin,
                      viewsets.ModelViewSet):
    """Возвращает список категорий и позволяет их добавлять и редактировать."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(AdminOrReadOnlyMixin,
                   SearchMixin,
                   PaginationMixin,
                   GetPostMixin,
                   SlugLookupMixin,
                   viewsets.ModelViewSet):
    """Возвращает список жанров и позволяет их добавлять и редактировать."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с отзывами.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def recalculate_rating(self, title):
        reviews = title.reviews.all()
        if reviews.exists():
            title.rating = sum([review.score for review in reviews]) / reviews.count()
        else:
            title.rating = None
        title.save()

    def get_post_id(self):
        """Возвращает id произведения."""
        return self.kwargs.get("title_id")

    def perform_create(self, serializer):
        """Создает рецензию, указывая произведение с id, переданным в URL."""
        title_id = self.get_post_id()
        title = get_object_or_404(Title, pk=title_id)
    
        if Review.objects.filter(author=self.request.user, title=title).exists():
            raise serializers.ValidationError({"detail": "У вас уже была рецензия на это произведение. Вы можете удалить ее и написать новую или внести изменения."})

        serializer.save(author=self.request.user, title=title)
        self.recalculate_rating(title)

    def perform_update(self, serializer):
        title = serializer.instance.title
        serializer.save()
        self.recalculate_rating(title)

    def perform_destroy(self, instance):
        title = instance.title
        instance.delete()
        self.recalculate_rating(title)

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
