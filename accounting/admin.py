from django.contrib import admin
from .models import Check, Salary, OutcomeType, Outcome, ExpenditureStaff


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'student', 'is_confirmed', ]
    list_display_links = ['id', ]


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'kpi_amount']
    list_display_links = ['id']


@admin.register(OutcomeType)
class OutcomeTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'limit', ]
    list_display_links = ['id', 'name', ]


@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'amount', ]
    list_display_links = ['id', 'type', ]


@admin.register(ExpenditureStaff)
class ExpenditureStaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', ]
    list_display_links = ['id', 'name', ]
