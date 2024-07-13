from django.db import models
from shared.models import BaseModel
from authentication.models import User
from lead.models import Student


class Check(BaseModel):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_confirmed_check = models.BooleanField(default=False)


class Salary(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    find = models.FloatField(default=0.0)
    debt = models.FloatField(default=0.0)
    kpi_amount = models.FloatField(default=0.0)
    total_salary = models.FloatField(default=0.0)


class OutcomeType(BaseModel):
    name = models.CharField(max_length=255)
    limit = models.FloatField(default=0.0)


class Outcome(BaseModel):
    outcome_type = models.ForeignKey(OutcomeType, on_delete=models.CASCADE)
    spent_amount = models.FloatField(default=0.0)
    rest_amount = models.FloatField(default=0.0)
