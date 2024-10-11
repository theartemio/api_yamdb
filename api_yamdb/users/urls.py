from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomTokenObtainView, RegistrationAPIView, UsersMeAPIView,
                    UsersViewSet)

router = DefaultRouter()
router.register("users", UsersViewSet)

urlpatterns = [
    path('auth/signup/', RegistrationAPIView.as_view()),
    path('auth/token/', CustomTokenObtainView.as_view(), name='custom_token_obtain'),
    path('users/me/', UsersMeAPIView.as_view()),
    path('', include(router.urls)),
]
