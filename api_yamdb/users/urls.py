from .views import RegistrationAPIView, LoginAPIView, UsersAPIView
from django.urls import path



urlpatterns = [
    # path('users/', include(router.urls)),
    path('auth/signup/', RegistrationAPIView.as_view()),
    path('auth/token/', LoginAPIView.as_view()),
    path('users/', UsersAPIView.as_view()),
]
