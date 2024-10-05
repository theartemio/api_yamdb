from rest_framework import serializers

from reviews.models import Review, Comment, Title


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
