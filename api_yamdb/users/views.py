import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions_q import IsAdmin
from .serializers import RegistrationSerializer, UsersMeSerializer


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions_q import IsAdmin
from .serializers import CustomTokenObtainSerializer

User = get_user_model()

class CustomTokenObtainView(APIView):
    """
    Вьюсет для получения токена.
    """
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
    Вьюсет для регистрации новых пользователей и отправки кода
    новым и старым пользователям.
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


    def post(self, request, *args, **kwargs):
        """
        Логика процесса регистрации:
        - Если существует пользователь с парой адрес электронной почты+имя пользователя, то код отправляется повторно.
        – Если передается неполная информация (имя пользователя или почта не совпадают с базой), возвраается ответ с кодом 400.
        - Если такого пользователя не существует, пользователь создается.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            try:
                user = User.objects.get(email=email)
                if user.username != username:
                    return Response(
                        {"error": "Имя пользователя не соответствует адресу почты."}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

            except User.DoesNotExist:
                try:
                    user = User.objects.get(username=username)
                    if user.email != email:
                        return Response(
                            {"error": "Почта не соответствует имени пользователя."},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except User.DoesNotExist:
                    user = User.objects.create(username=username, email=email)
            confirmation_code = random.randint(1000, 9999)
            user.confirmation_code = confirmation_code
            user.save()
            send_mail(
                subject='Code',
                message=f'Confirmation code: {confirmation_code}',
                from_email='api@yamdb.not',
                recipient_list=[user.email],
                fail_silently=True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersMeAPIView(APIView):
    """
    Позволяет пользователю просматривать информацию о себе и менять ее.
    Просмотр информации и ее изменение доступно только
    самому пользователю.
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
    Методы:
        Вьюсет работает только с методами GET и PATCH.
    """
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UsersMeSerializer  # Может не подойти
    filter_backends = (filters.SearchFilter, )
    lookup_field = 'username'
    search_fields = ('username',)