import datetime as dt

from rest_framework import serializers


def validate_year(value):
    """
    Проверяет что год выпуска произведения уже наступил
    (что произведение уже вышло)
    """
    current_year = dt.date.today().year
    if value > current_year:
        raise serializers.ValidationError("Произведение еще не вышло!")
    return value
