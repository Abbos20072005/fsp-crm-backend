from django.contrib import admin
from .models import Lead, Comment, Student, StudentDocuments, DocumentType


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone']
    list_filter = ['is_deleted']
    search_fields = ['name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone']
    list_filter = ['is_deleted']
    search_fields = ['full_name']


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['is_deleted']
    search_fields = ['name']


@admin.register(StudentDocuments)
class StudentDocumentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'info', 'document']
    list_filter = ['is_deleted']
    search_fields = ['name']

# Register your models here.
# admin.site.register(Lead, AdminLead)
# admin.site.register(Comment, AdminComment)
