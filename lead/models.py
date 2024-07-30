from django.db import models
from authentication.models import User
from core.BaseModel import BaseModel

STATUS_CHOICES = (
    (1, 'INTERESTED'),
    (2, 'POSSIBLE'),
    (3, 'JOINED'),
    (4, 'CANCELLED'),
)

SOURCE_CHOICES = (
    (1, 'INSTAGRAM'),
    (2, 'TELEGRAM'),
    (3, 'WEBSITE'),
    (4, 'OTHER'),
)


class Lead(BaseModel):
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=100)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, blank=True, null=True)
    address = models.CharField(max_length=100)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    source = models.IntegerField(choices=SOURCE_CHOICES, default=1, blank=True, null=True)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    comment = models.TextField()

    def __str__(self):
        return self.comment


class Student(BaseModel, models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    full_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=100)
    personal_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class DocumentType(BaseModel, models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class StudentDocuments(BaseModel, models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    info = models.CharField(max_length=250, blank=True, null=True)
    document = models.FileField(upload_to='document/', default='/None.jpg')

    class Meta:
        unique_together = ('student', 'document')
        ordering = ['name']

    def __str__(self):
        # return self.name
        return '%s: %s ' % (self.student, self.type)

