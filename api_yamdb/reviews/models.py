from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

User = get_user_model()


class NameSlugMixin(models.Model):
    """Миксин для простых моделей с двумя полями."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

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


    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre,
                                   related_name='genres')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 related_name="titles",
                                 null=True,
                                 blank=False
                                 )
    rating = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Модель для представления отзыва на произведение.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True
    )
    text = models.TextField()
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="reviews")
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review',
            )
        ]

        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    """
    Модель для представления комментария.
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.text[:50]
