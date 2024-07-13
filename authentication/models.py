from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    (1, 'Client'),
    (2, 'Admin'),
    (3, 'HR'),
    (4, 'SuperAdmin'),
)


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=1)

    def __str__(self):
        return self.username
