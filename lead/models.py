from django.db import models


class Lead(models.Model):
    STATUS_CHOICES = (
        (1, 'JOINED'),
        (2, 'INTERESTED')
    )

    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=2)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=100)
    personal_number = models.CharField(max_length=100)
    passport = models.CharField(max_length=100)
    father_passport = models.CharField(max_length=100)
    mother_passport = models.CharField(max_length=100)
