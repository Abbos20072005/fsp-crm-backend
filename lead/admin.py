from django.contrib import admin
from .models import Lead, Student, Comment


@admin.register(Lead)
class AdminLead(admin.ModelAdmin):
    list_display = ['name', 'is_deleted']


@admin.register(Student)
class AdminStudent(admin.ModelAdmin):
    list_display = ['full_name']


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['id', 'comment']
    list_display_links = ['id', 'comment']
