import random
import re
from http import HTTPStatus

# from .models import User
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import (AccessToken, BlacklistedToken,
                                             RefreshToken)

from .permissions import IsAdmin, IsModerator
from .serializers import (RegistrationSerializer,
                          UsersMeSerializer)

User = get_user_model()
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainSerializer
from .permissions import IsAdmin


class CustomTokenObtainView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'token': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class AdminPermissionMixin:
    """Миксин для проверки авторства и аутентификации."""
    permission_classes = (IsAdmin,)



class RegistrationAPIView(APIView):
    """
    Allow all users (authenticated and unauthenticated) access to this endpoint.
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle user registration or confirmation code resend via POST request.
        """
        username = request.data.get("username")
        email = request.data.get("email")

        # Check if user exists
        user, created = User.objects.get_or_create(username=username)

        # If user exists, update confirmation_code, otherwise create a new user
        confirmation_code = random.randint(1000, 9999)
        user.confirmation_code = confirmation_code
        user.email = email  # Update email only if you want to allow email changes
        user.save()

        # Send confirmation code
        send_mail(
            subject='Code',
            message=f'Confirmation code: {confirmation_code}',
            from_email='api@yamdb.not',
            recipient_list=[user.email],
            fail_silently=True,
        )

        return Response(status=status.HTTP_200_OK)



class UsersMeAPIView(APIView):
    """
    Позволяет пользователю просматривать информацию о себе и менять ее.

    Пермишены:
        Просмотр информации и ее изменение доступно только
        самому пользователю.
        Проверка осуществляется с помощью кастомного пермишена
        IsSameUserOrRestricted.
    Методы:
        Вьюсет работает только с методами GET и PATCH.
    """
    serializer_class = UsersMeSerializer
    
    def get(self, request):
        user = request.user
        serializer = UsersMeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = UsersMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersViewSet(
    AdminPermissionMixin,
    viewsets.ModelViewSet):
    """
    Вьюсет администратора, позволяет просматривать список пользователей,
    добавлять новых, удалять старых и менять информацию.

    Пермишены:
        Просмотр информации и ее изменение доступно только
        самому пользователю.
        Проверка осуществляется с помощью кастомного пермишена
        IsSameUserOrRestricted.
    Методы:
        Вьюсет работает только с методами GET и PATCH.
    """
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UsersMeSerializer  # Может не подойти
    filter_backends = (filters.SearchFilter, )
    lookup_field = 'username'
    search_fields = ('username',)
