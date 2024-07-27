from django.db import models
from core.BaseModel import BaseModel
from authentication.models import User
from django.core.validators import FileExtensionValidator
from lead.models import Student
from django.core.validators import MinValueValidator, MaxValueValidator


class Check(BaseModel):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    file = models.ImageField(upload_to='check_images/',
                             validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student}'


class Salary(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kpi_amount = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)


class ExpenditureStaff(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=777)
    amount = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)

    def __str__(self):
        return f'{self.name} {self.user.username}'


class OutcomeType(BaseModel):
    name = models.CharField(max_length=255)
    limit = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(50)])

    def __str__(self):
        return self.name


class Outcome(BaseModel):
    type = models.ForeignKey(OutcomeType, on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)

    def __str__(self):
        return f'{self.type.name}'
