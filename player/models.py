from django.db import models
from django.contrib.auth.models import AbstractUser

class Player(AbstractUser):
    username = models.CharField(max_length=50, unique=True, null=True)
    password = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True, unique=True)
    kingdom_name = models.CharField(max_length=100, null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'email']

    def __str__(self):
        return str(self.username)
