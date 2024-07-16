from django.db import models
from authentication.models import User


class Comment(models.Model):
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class Lead(models.Model):
    STATUS_CHOICES = (
        (1, 'JOINED'),
        (2, 'INTERESTED'),
        (3, 'PAYED'),
        (4, 'CANCELLED'),
    )

    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=2)
    address = models.CharField(max_length=100)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=100)
    personal_number = models.CharField(max_length=100)
    passport = models.FileField(upload_to='passport/')
    father_passport = models.FileField(max_length=100)
    mother_passport = models.FileField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
