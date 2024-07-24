from django.contrib import admin
from .models import Lead, Student


class AdminLead(admin.ModelAdmin):
    list_display = ['name', 'is_deleted']


class AdminStudent(admin.ModelAdmin):
    list_display = ['full_name']


admin.site.register(Lead, AdminLead)
admin.site.register(Student, AdminStudent)
