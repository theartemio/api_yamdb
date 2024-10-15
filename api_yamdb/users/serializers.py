from django.http import Http404
from rest_framework import serializers

from .constants import (
    MAX_EMAIL_L,
    MAX_ROLE_L,
    MAX_USER_NAMES_L,
    MAX_CODE_L,
    MAX_TOKEN_L,
)
from .mixins import ValidateUsernameMixin
from .models import User


class RegistrationSerializer(
    ValidateUsernameMixin, serializers.ModelSerializer
):
    """Сериализация регистрации юзера."""

    email = serializers.EmailField(
        required=True,
        max_length=MAX_EMAIL_L,
    )
    username = serializers.CharField(
        required=True,
        max_length=MAX_USER_NAMES_L,
    )

    class Meta:
        model = User
        fields = ["email", "username"]


class CustomTokenObtainSerializer(serializers.Serializer):
    """Кастомный сериализатор для получения токена."""

    username = serializers.CharField(write_only=True, required=True)
    confirmation_code = serializers.IntegerField(
        write_only=True, required=True
    )

    def validate(self, data):
        username = data.get("username")
        confirmation_code = data.get("confirmation_code")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError("Неверный код или юзернейм.")

        return {"user": user}


class UsersMeSerializer(ValidateUsernameMixin, serializers.ModelSerializer):

    first_name = serializers.CharField(
        max_length=MAX_USER_NAMES_L, required=False
    )
    last_name = serializers.CharField(
        max_length=MAX_USER_NAMES_L, required=False
    )
    role = serializers.CharField(max_length=MAX_ROLE_L, read_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        ]


class UsersSerializer(ValidateUsernameMixin, serializers.ModelSerializer):
    first_name = serializers.CharField(
        max_length=MAX_USER_NAMES_L, required=False
    )
    last_name = serializers.CharField(
        max_length=MAX_USER_NAMES_L, required=False
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "role",
            "first_name",
            "last_name",
            "bio",
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=MAX_EMAIL_L)
    username = serializers.CharField(
        max_length=MAX_USER_NAMES_L,
    )
    confirmate_code = serializers.CharField(
        max_length=MAX_CODE_L,
    )
    token = serializers.CharField(
        max_length=MAX_TOKEN_L,
    )
