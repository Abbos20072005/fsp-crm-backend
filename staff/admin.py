from django.contrib import admin
from staff.models import Admin,SuperAdmin,HR
@admin.register(Admin)
class Admin(admin.ModelAdmin):
    list_display = ('image','phone')
    # list_filter = ('hire_date')
@admin.register(HR)
class HR(admin.ModelAdmin):
    list_display = ('image','phone')
    # list_filter = ('hire_date')
@admin.register(SuperAdmin)
class SuperAdmin(admin.ModelAdmin):
    list_display = ('image','phone')
    # list_filter = ('hire_date')



# Register your models here.
