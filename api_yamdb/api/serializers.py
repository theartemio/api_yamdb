import datetime as dt

from rest_framework import serializers
from reviews.models import Category, Genre, Title, Review, Comment, Title


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
      
class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review (Отзыв).
    """
    title = serializers.PrimaryKeyRelatedField(queryset=Title.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'title', 'author', 'score', 'text', 'pub_date']
        read_only_fields = ['author', 'pub_date']

    def validate_score(self, value):
        """
        Проверка того, что оценка находится в диапазоне от 1 до 10.
        """
        if not (1 <= value <= 10):
            raise serializers.ValidationError(
                "Значение должно быть от 1 до 10."
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.
    """
    class Meta:
        model = Comment
        fields = ['id', 'review', 'author', 'text', 'pub_date']
        read_only_fields = ['author', 'pub_date']
     

