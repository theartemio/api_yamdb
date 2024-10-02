from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()  # temp user model


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
        переданных списком
    """
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name='genres')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 related_name="titles",
                                 null=True,
                                 blank=False
                                 )
    rating = models.PositiveSmallIntegerField(null=True)  # поле для рейтинга

    def __str__(self):
        return self.name
