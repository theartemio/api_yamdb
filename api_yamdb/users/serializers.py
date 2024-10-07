import random
import re

from rest_framework import serializers

# from .models import User
from django.contrib.auth import authenticate, get_user_model

from django.core.mail import send_mail

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    class Meta:
        model = User
        # Перечислить все поля, которые могут быть включены в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = ['email', 'username']
        # fields = '__all__'

    def create(self, validated_data):
        # Использовать метод create_user, который мы
        # написали ранее, для создания нового пользователя.
        """ confirmation_code = random.randint(1000, 9999)
        users_email = self.user.email
        send_mail(
            subject='Code',
            message=f'confirmation code: {confirmation_code}',
            from_email='api@yamdb.not',
            recipient_list=[users_email],
            fail_silently=True,
        ) """
        return User.objects.create_user(**validated_data)


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

    """ def create(self, validated_data):
        return User.objects.create_user(**validated_data) """


class UsersMeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150,)
    email = serializers.EmailField(max_length=254, required=False)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']

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
