from django.urls import path
from .views import HRViewSet

urlpatterns = [
    path('admins/<int:staff_id>/',
         HRViewSet.as_view({'get': 'list_admins', 'post': 'create_admin', 'delete': 'delete_admin'}), name=''),
]
