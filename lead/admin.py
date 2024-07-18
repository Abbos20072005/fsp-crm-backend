from django.contrib import admin
from .models import Lead, Student


class AdminLead(admin.ModelAdmin):
    list_display = ['name', 'is_deleted']


# Register your models here.
admin.site.register(Lead, AdminLead)
