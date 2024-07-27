from django.contrib import admin
from .models import Lead, Comment, Student, StudentDocuments, DocumentType

from .models import Lead, Student, Comment


@admin.register(Lead)
class AdminLead(admin.ModelAdmin):
    list_display = ['name', 'is_deleted']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['lead', 'full_name', 'phone', 'is_deleted']
    list_display_links = ['lead', 'full_name', 'phone', 'is_deleted']
    list_filter = ['is_deleted']
    search_fields = ['full_name', 'phone']


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['is_deleted']
    search_fields = ['name']


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['comment']
    list_display_links = ['comment']


