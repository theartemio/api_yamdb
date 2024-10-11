import re

from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import serializers

from .models import User

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализация регистрации юзера."""

    email = serializers.EmailField(required=True, max_length=254,)
    username = serializers.CharField(required=True, max_length=150,)

    class Meta:
        model = User
        fields = ['email', 'username']

    def validate_username(self, value):
        """
        Проверяет юзернейм по паттерну, а также не дает использовать
        юзернейм me.
        """
        pattern = r'^[\w.@+-]+\Z'
        if value == 'me' or not re.fullmatch(pattern, value):
            error_message = "Такое имя пользователя недопустимо!"
            raise serializers.ValidationError(error_message)
        return value


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


class UsersMeSerializer(serializers.ModelSerializer):

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

    def validate_username(self, value):
        pattern = r'^[\w.@+-]+\Z'
        if re.fullmatch(pattern, value) and value != 'me':
            return value
        raise serializers.ValidationError()


class UsersSerializer(serializers.ModelSerializer):
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

    def validate_username(self, value):
        pattern = r'^[\w.@+-]+\Z'
        if re.fullmatch(pattern, value) and value != 'me':
            return value
        raise serializers.ValidationError()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255,)
    confirmate_code = serializers.CharField(max_length=128,)
    token = serializers.CharField(max_length=255,)
