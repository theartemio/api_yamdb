import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, Title


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        fields = ("name", "slug",)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        fields = ("name", "slug",)
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            required=True,
                                            allow_null=True,
                                            slug_field="slug")
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field="slug",
                                         many=True,
                                         required=False,
                                         allow_null=True,
                                         )

    class Meta:
        fields = ("id",
                  "name",
                  "year",
                  "rating",
                  "description",
                  "genre",
                  "category")
        model = Title

    def validate(self, data):
        """
        Проверяет что год выпуска произведения уже наступил
        (что произведение уже вышло)
        """
        year = data["year"]
        current_year = dt.date.today().year
        if year > current_year:
            raise serializers.ValidationError(
                "Произведение еще не вышло!"
            )
        return data
