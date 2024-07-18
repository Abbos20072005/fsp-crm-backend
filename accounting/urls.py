from django.urls import path
from .views import CheckViewSet, OutcomeTypeViewSet, OutcomeViewSet

urlpatterns = [
    path('checks/<int:pk>/', CheckViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    path('student/<int:pk>/checks/', CheckViewSet.as_view({'get': 'student_checks'})),
    path('checks/', CheckViewSet.as_view({'get': 'list', 'post': 'create'})),

    path('outcometype/<int:pk>/', OutcomeTypeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('outcometypes/', OutcomeTypeViewSet.as_view({'get': 'list', 'post': 'create'})),

    path('outcome/<int:pk>/', OutcomeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('outcomes/', OutcomeViewSet.as_view({'get': 'list', 'post': 'create'})),

]

"""
/outcome - CR   +
/outcome/filter - type/fromToDate... +
/salary - list of admins with salaries      
/staff/:id - Retrieve
/check :id - RetrieveUpdate   +
/check/:leadId - list of checks by leadId   +



"""
