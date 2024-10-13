import re

from django.http import Http404
from rest_framework import serializers

from .models import User

PATTERN = r'^[\w.@+-]+\Z'


class ValidateUsernameMixin:
    """Миксин для валидации поля username."""

    def validate_username(self, value):
        """
        Проверяет юзернейм по паттерну, а также не дает использовать
        юзернейм me.
        """
        if value == 'me' or not re.fullmatch(PATTERN, value):
            error_message = "Такое имя пользователя недопустимо!"
            raise serializers.ValidationError(error_message)
        return value


class RegistrationSerializer(ValidateUsernameMixin,
                             serializers.ModelSerializer):
    """Сериализация регистрации юзера."""

    email = serializers.EmailField(required=True, max_length=254,)
    username = serializers.CharField(required=True, max_length=150,)

    class Meta:
        model = User
        fields = ['email', 'username']


class CustomTokenObtainSerializer(serializers.Serializer):
    """Кастомный сериализатор для получения токена."""
    username = serializers.CharField(write_only=True, required=True)
    confirmation_code = serializers.IntegerField(write_only=True,
                                                 required=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError('Неверный код или юзернейм.')

        return {'user': user}


class UsersMeSerializer(ValidateUsernameMixin, serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    role = serializers.CharField(max_length=16, read_only=True)

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role']


class UsersSerializer(ValidateUsernameMixin, serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'role',
                  'first_name',
                  'last_name',
                  'bio']


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255,)
    confirmate_code = serializers.CharField(max_length=128,)
    token = serializers.CharField(max_length=255,)
