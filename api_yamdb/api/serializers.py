import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


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
                                            slug_field="slug",
                                            write_only=True)
    
    category_detail = CategorySerializer(source='category', read_only=True)


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
                  "category",
                  "category_detail")
        model = Title
    

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('category', None)
        return ret

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
    title = serializers.PrimaryKeyRelatedField(queryset=Title.objects.all(),
                                               required=False)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)


    class Meta:
        model = Review
        fields = ['id', 'title', 'text', 'author', 'score', 'pub_date']
        read_only_fields = ['author', 'pub_date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('title', None)
        return representation


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
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all(),
                                                required=False)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('review', None)
        return representation

    class Meta:
        model = Comment
        fields = ['id', 'review', 'text', 'author', 'pub_date']
        read_only_fields = ['author', 'pub_date']
