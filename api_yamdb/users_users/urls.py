from .views import RegistrationAPIView, UsersAPIView, UsersMeAPIView, UserDetail, UsersViewSet, UsersMeViewSet, UsersMe, LoginViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
# router.register('me', UsersMeViewSet, basename='me')

urlpatterns = [
    # path('users/', include(router.urls)),
    path('auth/signup/', RegistrationAPIView.as_view()),
    path('auth/token/', LoginViewSet.as_view({'post': 'create', })),
    # path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('users/', UsersAPIView.as_view()),
    path('users/', UsersViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('users/me/', UsersMe.as_view()),
    path('users/me/', UsersMeAPIView.as_view()),
    # path('users/me/', UsersMeViewSet.as_view({'get': 'retrieve', 'patch': 'update'})),
    # path('users/me/', UsersMeViewSet.as_view({'get': 'retrieve'})),
    path('users/<slug:username>/', UserDetail.as_view()),
]
