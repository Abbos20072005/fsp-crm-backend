from django.contrib import admin
from .models import Check, Salary, OutcomeType, Outcome


class CheckAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'student', 'is_confirmed', ]
    list_display_links = ['id', ]


class SalaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'kpi_amount']
    list_display_links = ['id']


class OutcomeTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'limit', ]
    list_display_links = ['id', 'name', ]


class OutcomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'amount', ]
    list_display_links = ['id', 'type', ]


admin.site.register(Check, CheckAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(OutcomeType, OutcomeTypeAdmin)
admin.site.register(Outcome, OutcomeAdmin)

