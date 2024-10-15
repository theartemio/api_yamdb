from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        fields = (
            "name",
            "slug",
        )
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        fields = (
            "name",
            "slug",
        )
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при просмотре списком."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        required=True,
        slug_field="slug",
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field="slug",
        many=True,
        required=True,
        allow_null=False,
        allow_empty=False,
    )
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )


class TitleDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра произведений."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review (Отзыв).
    """

    title = serializers.PrimaryKeyRelatedField(
        queryset=Title.objects.all(), required=False
    )
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Review
        fields = ("id", "title", "text", "author", "score", "pub_date")
        read_only_fields = ("author", "pub_date")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("title", None)
        return representation

    def validate_score(self, value):
        """
        Проверка того, что оценка находится в диапазоне от 1 до 10.
        """
        if not (1 <= value <= 10):
            raise serializers.ValidationError(
                "Значение должно", "быть от 1 до 10."
            )
        return value

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            title_id = self.context["view"].kwargs.get("title_id")
            title = get_object_or_404(Title, pk=title_id)

            if request.method == 'POST' and Review.objects.filter(
                author=self.context["request"].user, title=title
            ).exists():
                raise serializers.ValidationError(
                    {
                        "detail": (
                            "У вас уже была рецензия на это произведение. "
                            "Вы можете ее изменить или удалить "
                            "и написать новую."
                        )
                    }
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.
    """

    review = serializers.PrimaryKeyRelatedField(
        queryset=Review.objects.all(), required=False
    )
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "review",
            "text",
            "author",
            "pub_date",
        )
        read_only_fields = (
            "author",
            "pub_date",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("review", None)
        return representation
