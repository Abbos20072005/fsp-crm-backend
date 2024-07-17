from django.urls import path
from .views import CheckViewSet, OutcomeTypeViewSet, OutcomeViewSet

urlpatterns = [
    path('checks/<int:pk>/', CheckViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    path('student/<int:pk>/checks/', CheckViewSet.as_view({'get': 'student_checks'})),
    path('checks/create/', CheckViewSet.as_view({'post': 'create'})),
    path('checks/', CheckViewSet.as_view({'get': 'list'})),

    path('outcometype/<int:pk>/', OutcomeTypeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('outcometype/create/', OutcomeTypeViewSet.as_view({'post': 'create'})),
    path('outcometypes/', OutcomeTypeViewSet.as_view({'get': 'list'})),

    path('outcome/<int:pk>/', OutcomeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('outcome/create/', OutcomeViewSet.as_view({'post': 'create'})),
    path('outcomes/', OutcomeViewSet.as_view({'get': 'list'})),

]

"""
/outcome - CR   +
/outcome/filter - type/fromToDate...
/salary - list of admins with salaries      
/staff/:id - Retrieve
/check :id - RetrieveUpdate   +
/check/:leadId - list of checks by leadId   +
"""
