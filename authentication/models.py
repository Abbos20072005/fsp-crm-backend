from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    (1, 'Admin'),
    (2, 'Accountant'),
    (3, 'HR'),
    (4, 'SuperAdmin'),
)


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=1)
    kpi = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    fixed_salary = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class BlacklistedAccessToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)