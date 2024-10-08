from api.permissions import IsAuthorOrStaff
from api.serializers import CommentSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Category, Comment, Genre, Review, Title
from users.permissions_q import IsAdminOrReadonly, IsAuthorOrReadOnly, IsModeratorOrAdmin

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

class AuthorPermissionMixin:
    """Миксин для проверки авторства и аутентификации."""
    # permission_classes = (IsAuthOrReadOnly,)
    pass

class AdminOrReadOnlyMixin:
    """Миксин для проверки админства."""
    permission_classes = (IsAdminOrReadonly, )
    


class AuthorMixin:
    """Миксин для проверки авторства."""
    permission_classes = [IsAuthenticatedOrReadOnly,]


class TitleViewSet(AdminOrReadOnlyMixin,
                   PaginationMixin, viewsets.ModelViewSet):
    """Возвращает список тайтлов, позволяет их добавлять и редактировать."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')


class CategoryViewSet(AdminOrReadOnlyMixin,
                      SearchMixin,
                      PaginationMixin,
                      GetPostMixin,
                      SlugLookupMixin,
                      viewsets.ModelViewSet):
    """Возвращает список категорий и позволяет их добавлять и редактировать."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(AdminOrReadOnlyMixin,
                   SearchMixin,
                   PaginationMixin,
                   GetPostMixin,
                   SlugLookupMixin,
                   viewsets.ModelViewSet):
    """Возвращает список жанров и позволяет их добавлять и редактировать."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с отзывами.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly, IsModeratorOrAdmin] 

    def get_post_id(self):
        """Возвращает id произведения."""
        return self.kwargs.get("title_id")

    def perform_create(self, serializer):
        """Создает рецензию, указывая произведение с id, переданным в URL."""
        title_id = self.get_post_id()
        title = get_object_or_404(Title, pk=title_id)
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
    permission_classes = [IsAuthorOrReadOnly, IsModeratorOrAdmin]

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
