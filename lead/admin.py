from django.contrib import admin
from .models import Lead, Comment, Student, StudentDocuments, DocumentType


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone']
    list_filter = ['is_deleted']
    search_fields = ['name']


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


@admin.register(StudentDocuments)
class StudentDocumentsAdmin(admin.ModelAdmin):
    list_display = ['student', 'name', 'document']
    list_filter = ['is_deleted']
    search_fields = ['name']
