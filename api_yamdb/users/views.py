import random

from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdminOrRestricted
from .serializers import (
    CustomTokenObtainSerializer,
    RegistrationSerializer,
    UsersMeSerializer,
    UsersSerializer,
)


class CustomTokenObtainView(APIView):
    """
    Вьюсет для получения токена.
    """

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "token": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class AdminPermissionMixin:
    """Миксин для проверки администраторов и суперпользователей."""

    permission_classes = (IsAdminOrRestricted,)


class RegistrationAPIView(APIView):
    """
    Вьюсет для регистрации новых пользователей и отправки кода
    подтверждения новым и старым пользователям.
    """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def generate_confirmation_code(self):
        return random.randint(1000, 9999)

    def post(self, request, *args, **kwargs):
        """
        Логика процесса регистрации:
        - Если существует пользователь с парой
        адрес электронной почты+имя пользователя, то код отправляется повторно.
        – Если передается неполная информация (имя пользователя или почта
        не совпадают с базой), возвращается ответ с кодом 400.
        - Если такого пользователя не существует, пользователь создается.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            email = serializer.validated_data.get("email")
            confirmation_code = self.generate_confirmation_code()
            try:
                user, created = User.objects.get_or_create(
                    username=username, defaults={"email": email}
                )
            except IntegrityError:
                return Response(
                    {"error": "Эмейл занят!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not created and user.email != email:
                return Response(
                    {"error": "Эмейл не соответствует имени пользователя!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.confirmation_code = confirmation_code
            user.save()
            send_mail(
                subject="Code",
                message=f"Confirmation code: {confirmation_code}",
                from_email="api@yamdb.not",
                recipient_list=[email],
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


class UsersViewSet(AdminPermissionMixin, viewsets.ModelViewSet):
    """
    Вьюсет просмотра списка пользователей администраторами.
    Позволяет админу просматривать список пользователей,
    добавлять новых, удалять старых и менять информацию.
    """

    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = "username"
    search_fields = ("username",)
