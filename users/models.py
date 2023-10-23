from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
