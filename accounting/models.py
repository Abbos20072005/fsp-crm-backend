from django.db import models
from shared.models import BaseModel


class CheckStudents(models.Model, BaseModel):
    student = models.ForeignKey('lead.Student', on_delete=models.CASCADE)
    check_is_confirmed = models.BooleanField(default=False)
