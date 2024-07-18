from django.db import models
from authentication.models import User
from core.BaseModel import BaseModel


class Lead(BaseModel):
    STATUS_CHOICES = (
        (1, 'INTERESTED'),
        (2, 'POSSIBLE'),
        (3, 'JOINED'),
        (4, 'CANCELLED'),
    )

    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=1)
    address = models.CharField(max_length=100)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)

    comment = models.TextField()

    def __str__(self):
        return self.comment


class Student(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=100)
    personal_number = models.CharField(max_length=100)
    passport = models.FileField(upload_to='passport/')
    father_passport = models.FileField(upload_to='passport/')
    mother_passport = models.FileField(upload_to='passport/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
