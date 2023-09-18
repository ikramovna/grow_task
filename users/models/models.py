from django.contrib.auth.models import AbstractUser
from django.db import models

# from users.models.base import BaseAbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)