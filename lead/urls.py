from django.urls import path
from .views import LeadViewSet

urlpatterns = [
    path('lead/', LeadViewSet.as_view({'post': 'create'})),
]

"""
/filter - all/status/admin/..filter by fields
/lead/:id - CRUD
/lead/:id/comment - Create
/student/:id - CRUD
/student/:id/upload - Upload Check File


"""

