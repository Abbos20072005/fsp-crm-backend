from django.db import models

STATUS_CHOICES = (
    (1, 'JOINED'),
    (2, 'INTERESTED'),
    (3, 'PAYED'),
    (4, 'CANCELLED')
)


class Lead(models.Model):
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=100)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    address = models.CharField(max_length=100)
    admin = models.ForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    pass


class Student(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=100)
    personal_number = models.CharField(max_length=100)
    passport = models.CharField(max_length=100)
    father_passport = models.CharField(max_length=100)
    mother_passport = models.CharField(max_length=100)
    ...





