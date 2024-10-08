import random
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, AbstractUser,
                                        BaseUserManager, PermissionsMixin)
from django.db import models

CHOICES = (
    ("user", "user"),
    ("moderator", "moderator"),
    ("admin", "admin"),
)


class UserManager(BaseUserManager):


    def create_user(self, username, email, role='user', bio='1', password=None):
        code = random.randint(1000, 9999)
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=role,
            bio=bio,
            confirmate_code=code,
        )
        user.save()
        return user

    def create_superuser(self, username, email, role='user', bio='1', password=None):
        user = self.create_user(username, email)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    password = None
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150,)
    last_name = models.CharField(max_length=150,)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=16, choices=CHOICES, default='user')
    confirmate_code = models.CharField(max_length=4,)
    objects = UserManager()

    def __str__(self):
        return self.email
