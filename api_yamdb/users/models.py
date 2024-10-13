from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

CHOICES = (
    ("user", "user"),
    ("moderator", "moderator"),
    ("admin", "admin"),
)


class UserManager(BaseUserManager):

    def create_user(self, username, email, role='user', bio='', password=None):
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=role,
            bio=bio,
        )
        user.save()
        return user

    def create_superuser(self, username, email,
                         role='admin', bio='', password=None):
        user = self.create_user(username, email)
        user.is_superuser = True
        user.is_staff = True
        user.role = role
        user.save()
        return user


class User(AbstractUser):
    confirmation_code = models.SmallIntegerField(blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150,)
    last_name = models.CharField(max_length=150,)
    role = models.CharField(max_length=16, choices=CHOICES, default='user')
    bio = models.TextField(blank=True,)
    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def __str__(self):
        return self.email


User = get_user_model()
