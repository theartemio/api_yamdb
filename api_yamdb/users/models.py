from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from .constants import (ADMIN, CHOICES, MAX_EMAIL_L, MAX_ROLE_L,
                        MAX_USER_NAMES_L, MODERATOR, USER)


class UserManager(BaseUserManager):

    def create_user(self, username, email, role=USER, bio="", password=None):
        if username is None:
            raise TypeError("Укажите юзернейм.")
        if email is None:
            raise TypeError("Укажите эмейл.")
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=role,
            bio=bio,
        )
        user.save()
        return user

    def create_superuser(
        self, username, email, role=ADMIN, bio="", password=None
    ):
        user = self.create_user(username, email)
        user.is_superuser = True
        user.is_staff = True
        user.role = role
        user.save()
        return user


class User(AbstractUser):
    confirmation_code = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Код подтверждения.",
        help_text=(
            "Присылается на почту при регистрации.",
            " Используется для получения токена.",
        ),
    )
    email = models.EmailField(
        max_length=MAX_EMAIL_L,
        unique=True,
        verbose_name="Эмейл.",
        help_text=("Эмейл, он должен работать и принимать почту.",),
    )
    username = models.CharField(max_length=MAX_USER_NAMES_L, unique=True)
    first_name = models.CharField(
        max_length=MAX_USER_NAMES_L,
        verbose_name="Имя.",
        help_text="Имя, желательно настоящее.",
    )
    last_name = models.CharField(
        max_length=MAX_USER_NAMES_L,
        verbose_name="Фамилия.",
        help_text="Фамилия, тоже желательно настоящая.",
    )
    role = models.CharField(
        max_length=MAX_ROLE_L,
        choices=CHOICES,
        default=USER,
        verbose_name="Пользовательская роль.",
        help_text=(
            "Пользователь может быть модератором,",
            " админом или обычным юзером.",
        ),
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Биография.",
        help_text="Факты, которые пользователь хочет рассказать о себе.",
    )
    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.email
