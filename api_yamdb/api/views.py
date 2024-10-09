from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.permissions import IsAuthOrReadOnly
from api.serializers import CommentSerializer, ReviewSerializer
from reviews.models import Category, Comment, Genre, Review, Title
from users.permissions import IsAdminOrReadonly

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer

class IsModerator(permissions.BasePermission):
    """
    Пермишен для модератора.
    """
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if request.user.is_superuser:
                return True
            if request.user.role == 'moderator':
                return True
            return False
    def has_object_permission(self, request, view, obj):
        return True
        # return request.user.role == 'admin'


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
    """Миксин для проверки авторства и аутентификации."""
    permission_classes = (IsAuthOrReadOnly,)


class AdminOrReadOnlyMixin:
    """Миксин для проверки админства."""
    permission_classes = (IsAdminOrReadonly, )


class AuthorMixin:
    """Миксин для проверки авторства."""
    permission_classes = [IsAuthenticatedOrReadOnly,]


class TitleViewSet(AdminOrReadOnlyMixin,
                   PaginationMixin, viewsets.ModelViewSet):
    """Возвращает список тайтлов, позволяет их добавлять и редактировать."""
    # queryset = Title.objects.select_related('category').all()
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    http_method_names = ['get', 'post', 'patch', 'delete']
    


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
