import jwt
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser, AbstractUser
from datetime import datetime, timedelta
from django.conf import settings
from django.db import models

CHOICES = (
    ("user", "user"),
    ("moderator", "moderator"),
    ("admin", "admin"),
)


class UserManager(BaseUserManager):

    def create_user(self, username, email, role='user', bio='1', password=None):
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
    
    objects = UserManager()

    def __str__(self):
        return self.email


""" class User(AbstractBaseUser, PermissionsMixin):

    # username = models.CharField(db_index=True, max_length=255)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150,)
    last_name = models.CharField(max_length=150,)
    bio = models.CharField(max_length=255)
    role = models.CharField(max_length=16, choices=CHOICES, default='user')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
 """
