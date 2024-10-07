from .views import RegistrationAPIView, LoginAPIView, UsersAPIView, UsersMeAPIView, UserDetail, UsersViewSet, UsersMeViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('me', UsersMeViewSet, basename='me')

urlpatterns = [
    # path('users/', include(router.urls)),
    path('auth/signup/', RegistrationAPIView.as_view()),
    path('auth/token/', LoginAPIView.as_view()),
    # path('users/', UsersAPIView.as_view()),
    path('users/', UsersViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('users/me/', UsersMeAPIView.as_view()),
    # path('users/me/', UsersMeViewSet.as_view({'get': 'retrieve', 'patch': 'update'})),
    # path('users/me/', UsersMeViewSet.as_view({'get': 'retrieve'})),
    path('users/<slug:username>/', UserDetail.as_view()),
    
    
]
