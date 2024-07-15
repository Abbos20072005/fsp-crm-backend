from django.db import models
from shared.models import BaseModel
from authentication.models import User
# from lead.models import Student


class Check(BaseModel):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = ...
    file = ...
    student = models.ForeignKey('lead.Student', on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)


class Salary(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    find = models.FloatField(default=0.0)
    debt = models.FloatField(default=0.0)
    kpi_amount = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)


class OutcomeType(BaseModel):
    name = models.CharField(max_length=255)
    limit = models.FloatField(default=0.0)


class Outcome(BaseModel):
    type = models.ForeignKey(OutcomeType, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
