import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework import serializers
from users.models import User

from .constants import MAX_NAME_L, MAX_SLUG_L


class NameSlugMixin(models.Model):
    """Миксин для простых моделей с двумя полями."""

    name = models.CharField(max_length=MAX_NAME_L, verbose_name="Название")
    slug = models.SlugField(
        unique=True,
        max_length=MAX_SLUG_L,
        verbose_name="Слаг",
        help_text=(
            "Уникальный слаг, по которому можно указать жанр",
            "или категорию. Рекомендуется использовать понятный",
            "слаг, например транслитерацию или английское название.",
        ),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(NameSlugMixin, models.Model):
    """Модель для хранения категорий."""

    pass


class Genre(NameSlugMixin, models.Model):
    """Модель для хранения жанров."""

    pass


class Title(models.Model):
    """
    Модель для хранения произведений.
    Модель связана с моделями Category, Genre:
        - Поле category (необязательное) связано с моделью Category,
        - Поле genre (необязательное) связано с моделью Genre,
        у одного произведения допускается несколько жанров,
        переданных списком.
    """

    name = models.CharField(
        max_length=MAX_NAME_L,
        verbose_name="Название",
        help_text="Официальное название произведения.",
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="Год", help_text="Год выпуска произведения."
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Краткое описание произведения.",
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="genres",
        verbose_name="Жанры",
        help_text=("Жанры, к которым относится произведение.",
                   " Может быть несколько."),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="categories",
        null=True,
        blank=False,
        verbose_name="Категория",
        help_text="Категория, например 'фильм' или 'музыка'.",
    )
    rating = models.PositiveSmallIntegerField(
        null=True,
        verbose_name="Рейтинг",
        help_text=("Средний рейтинг. Считается по",
                   " всем опубликованным рецензиям."),
    )

    def clean(self):
        current_year = dt.date.today().year
        if self.year > current_year:
            raise serializers.ValidationError("Произведение еще не вышло!")

    def __str__(self):
        return f"{self.name} {self.genre} {self.category}"


class Review(models.Model):
    """
    Модель для представления отзыва на произведение.
    """

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews", null=True
    )
    text = models.TextField()
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        old_score = None
        if self.pk:
            old_score = (
                Review.objects.filter(pk=self.pk)
                .values_list("score", flat=True)
                .first()
            )
        super().save(*args, **kwargs)
        if old_score != self.score:
            self.title.recalculate_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.title.recalculate_rating()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],
                name="unique_review",
            )
        ]

        ordering = ["-pub_date"]

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    """
    Модель для представления комментария.
    """

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["pub_date"]

    def __str__(self):
        return self.text[:50]
