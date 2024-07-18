from django.contrib import admin
from .models import Lead, Comment


class AdminLead(admin.ModelAdmin):
    list_display = ['name', 'is_deleted']


class AdminComment(admin.ModelAdmin):
    list_display = ['name', 'is_deleted']


# Register your models here.
admin.site.register(Lead, AdminLead)
admin.site.register(Comment, AdminComment)
