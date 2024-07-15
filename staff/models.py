from django.db import models
from datetime import datetime
# from authentication.models import User
class Admin(models.Model):
    full_name = models.CharField(max_length=50)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=14)
    image = models.ImageField(upload_to='media/')
    date_of_birth = models.DateField(default=datetime.now)
    hire_date = models.DateField(default=datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class HR(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=14)
    image = models.ImageField(upload_to='media')
    date_of_birth = models.DateField(default=datetime.now)
    hire_date = models.DateField(default=datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class SuperAdmin(models.Model):
    full_name = models.CharField(max_length=50)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=14)
    image = models.ImageField(upload_to='media')
    date_of_birth = models.DateField(default=datetime.now)
    hire_date = models.DateField(default=datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name



