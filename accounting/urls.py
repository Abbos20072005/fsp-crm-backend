from django.urls import path
from .views import (CheckRetrieveUpdateAPIView, CheckListAPIView, CheckStudentListAPIView, OutcomeTypeListCreateAPIView,
                    OutcomeTypeDestroy, CheckDestroy, OutcomeListCreateAPIView)

urlpatterns = [
    path('checks/<int:pk>/', CheckRetrieveUpdateAPIView.as_view()),
    path('checks/', CheckListAPIView.as_view()),
    path('student/<int:pk>/checks', CheckStudentListAPIView.as_view()),
    path('outcometypes/', OutcomeTypeListCreateAPIView.as_view()),
    path('outcometypes/<int:pk>/', OutcomeTypeDestroy.as_view()),
    path('checks/<int:pk>/', CheckDestroy.as_view()),
    path('outcome', OutcomeListCreateAPIView.as_view())
]

"""
/outcome - CR   +
/outcome/filter - type/fromToDate...
/salary - list of admins with salaries      
/staff/:id - Retrieve
/check :id - RetrieveUpdate   +
/check/:leadId - list of checks by leadId   +
"""
