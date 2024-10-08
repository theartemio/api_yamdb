import random
import re

from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового."""

    class Meta:
        model = User
        fields = ['email', 'username']

    def create(self, validated_data):
        confirmation_code = random.randint(1000, 9999)  # Generate the confirmation code
        validated_data['confirmation_code'] = confirmation_code  # Add it to validated data
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        """
        Проверяет что username не равен me
        """
        if value == 'me':
            raise serializers.ValidationError(
                "Имя me запрещено!"
            )
        return value


class CustomTokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    confirmation_code = serializers.IntegerField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid username or confirmation code.')

        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError('Invalid username or confirmation code.')

        return {'user': user}


class UsersMeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, read_only=True)
    email = serializers.EmailField(max_length=254, required=False)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']


'''
class UsersSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=150, )
    # email = serializers.EmailField(max_length=254, )
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']

    def validate_username(self, value):
        pattern = r'^[\w.@+-]+\Z'
        if re.fullmatch(pattern, value):
            return value
        raise serializers.ValidationError()


class TokenObtainWithConfirmationCodeSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=True)  # Add username field
    confirmation_code = serializers.IntegerField(required=True)  # Add confirmation_code field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)  # Remove the password field requirement

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username
        return token

    def validate(self, attrs):
        print(attrs)  # Should show both username and confirmation_code now
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this username does not exist.')

        # Make sure you check the confirmation code
        if user.confirmation_code != int(confirmation_code):
            raise serializers.ValidationError('Invalid confirmation code.')

        attrs['user'] = user  # Store user for later use
        return super().validate(attrs)
'''


""" def create(self, validated_data):
        return User.objects.create_user(**validated_data) """





class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255,)
    confirmate_code = serializers.CharField(max_length=128,)
    token = serializers.CharField(max_length=255,)

    """ def validate(self, data):
        # В методе validate мы убеждаемся, что текущий экземпляр
        # LoginSerializer значение valid. В случае входа пользователя в систему
        # это означает подтверждение того, что присутствуют адрес электронной
        # почты и то, что эта комбинация соответствует одному из пользователей.
        email = data.get('email', None)
        username = data.get('username', None)

        # Вызвать исключение, если не предоставлена почта.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Метод authenticate предоставляется Django и выполняет проверку, что
        # предоставленные почта и пароль соответствуют какому-то пользователю в
        # нашей базе данных. Мы передаем email как username, так как в модели
        # пользователя USERNAME_FIELD = email.
        user = authenticate(username=username,)

        # Если пользователь с данными почтой/паролем не найден, то authenticate
        # вернет None. Возбудить исключение в таком случае.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django предоставляет флаг is_active для модели User. Его цель
        # сообщить, был ли пользователь деактивирован или заблокирован.
        # Проверить стоит, вызвать исключение в случае True.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # Метод validate должен возвращать словать проверенных данных. Это
        # данные, которые передются в т.ч. в методы create и update.
        return {
            'token': user.token
        } """
