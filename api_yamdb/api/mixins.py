from users.permissions import IsAdminOrReadonly, IsAuthOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters, response, status


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
    http_method_names = ("get", "post", "delete",)

    def retrieve(self, request, *args, **kwargs):
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SearchAndFilterMixin:
    """Миксин для поиска по имени и фильтрации по слагу."""
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
