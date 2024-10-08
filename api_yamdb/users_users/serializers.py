import random
import re

from rest_framework import serializers

# from .models import User
from django.contrib.auth import authenticate, get_user_model

from django.core.mail import send_mail

User = get_user_model()

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, )
    email = serializers.EmailField(max_length=254, )

    def create(self, validated_data):
        return super().create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        return instance

""" class RegistrationSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        # Перечислить все поля, которые могут быть включены в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = ['email', 'username']
        # fields = '__all__'

    def create(self, validated_data):
        # Использовать метод create_user, который мы
        # написали ранее, для создания нового пользователя.
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        return instance """


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


class UsersMeSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=150,)
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
    confirmate_code = serializers.CharField(max_length=5,)
    # token = serializers.CharField(max_length=255,)