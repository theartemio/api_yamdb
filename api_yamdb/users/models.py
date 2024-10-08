from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, AbstractUser,
                                        BaseUserManager, PermissionsMixin)
from django.db import models
from django.contrib.auth.hashers import make_password

CHOICES = (
    ("user", "user"),
    ("moderator", "moderator"),
    ("admin", "admin"),
)

class User(AbstractUser):
    confirmation_code = models.SmallIntegerField(blank=True, null=True)
    role = models.CharField(max_length=16, choices=CHOICES, default='user')
    bio = models.TextField(blank=True, null=True)
    # objects = UserManager()

    def __str__(self):
        return self.email

