from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

    def average_rating(self):
        """
        Метод для расчета среднего рейтинга произведения.
        """
        reviews = self.reviews.all()
        if reviews.exists():
            return sum(review.score for review in reviews) / reviews.count()
        return 0


class Review(models.Model):
    """
    Модель для представления отзыва на произведение.
    """
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True
    )

    text = models.TextField()
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'user_id'],
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
    user_id = models.IntegerField()
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.text[:50]
