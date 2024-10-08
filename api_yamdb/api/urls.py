from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router = DefaultRouter()
router.register("titles", TitleViewSet)

router.register("genres", GenreViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

categories_list = CategoryViewSet.as_view({
    "get": "list",
    "post": "create"
})
category_detail = CategoryViewSet.as_view({
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy"
})



urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include('users.urls')),
    path("v1/categories/<int:id>/",
         category_detail,
         name="category-detail"),
    path("v1/categories/",
         categories_list,
         name="categories-list")     
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

