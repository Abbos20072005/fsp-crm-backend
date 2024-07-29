from django.urls import path
from .views import (CheckViewSet, OutcomeTypeViewSet, OutcomeViewSet, OutcomeFilterViewSet, ExpenditureStaffViewSet,
                    CheckFilterViewSet, AdminCheckFilterViewSet)

urlpatterns = [
    path('check/<int:pk>/',
         CheckViewSet.as_view({'patch': 'confirm_check'})),
    path('checks/', CheckViewSet.as_view({'post': 'create'})),

    path('outcome-type/<int:pk>/',
         OutcomeTypeViewSet.as_view({'patch': 'update'})),
    path('outcome-types/', OutcomeTypeViewSet.as_view({'get': 'list', 'post': 'create'})),

    path('outcome/<int:pk>/', OutcomeViewSet.as_view({'get': 'retrieve', 'patch': 'update'})),
    path('outcomes/', OutcomeViewSet.as_view({'get': 'list', 'post': 'create'})),

    path('outcome/filter/', OutcomeFilterViewSet.as_view({'get': 'outcome_filter'})),

    path('expenditure-staff/<int:pk>/',
         ExpenditureStaffViewSet.as_view({'get': 'retrieve', 'patch': 'update', 'post': 'create'})),
    path('expenditure-staff/', ExpenditureStaffViewSet.as_view({'get': 'list'})),

    path('check/filter/', CheckFilterViewSet.as_view({'get': 'check_filter'})),
    path('admin-check/filter/', AdminCheckFilterViewSet.as_view({'get': 'check_by_admin_filter'})),

]

"""
/outcome - CR   +
/outcome/filter - type/fromToDate... +
/salary - list of admins with salaries      
/staff/:id - Retrieve    
/check :id - RetrieveUpdate   +
/check/:leadId - list of checks by leadId   +


"""
