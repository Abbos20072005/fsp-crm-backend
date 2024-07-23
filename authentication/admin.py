from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'role', 'kpi', 'fixed_salary')


admin.site.register(User)
