from django.urls import path
from .views import CheckViewSet, OutcomeTypeViewSet, OutcomeViewSet, OutcomeFilterViewSet, ExpenditureStaffViewSet

urlpatterns = [
    path('checks/<int:pk>/', CheckViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    path('student/<int:pk>/checks/', CheckViewSet.as_view({'get': 'student_checks'})),
    path('checks/', CheckViewSet.as_view({'get': 'list', 'post': 'create'})),

    path('outcome-type/<int:pk>/',
         OutcomeTypeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('outcome-types/', OutcomeTypeViewSet.as_view({'get': 'list', 'post': 'create'})),

    path('outcome/<int:pk>/', OutcomeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('outcomes/', OutcomeViewSet.as_view({'get': 'list', 'post': 'create'})),

    path('outcome/filter/', OutcomeFilterViewSet.as_view({'get': 'outcome_filter'})),

    path('expenditure-staff/<int:pk>/',
         ExpenditureStaffViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('expenditure/', ExpenditureStaffViewSet.as_view({'get': 'list', 'post': 'create'})),
]

"""
/outcome - CR   +
/outcome/filter - type/fromToDate... +
/salary - list of admins with salaries      
/staff/:id - Retrieve
/check :id - RetrieveUpdate   +
/check/:leadId - list of checks by leadId   +



"""
