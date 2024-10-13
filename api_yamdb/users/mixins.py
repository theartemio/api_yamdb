import re

from rest_framework import serializers

from .constants import PATTERN


class ValidateUsernameMixin:
    """Миксин для валидации поля username."""

    def validate_username(self, value):
        """
        Проверяет юзернейм по паттерну, а также не дает использовать
        юзернейм me.
        """
        if value == "me" or not re.fullmatch(PATTERN, value):
            error_message = "Такое имя пользователя недопустимо!"
            raise serializers.ValidationError(error_message)
        return value
