from django.urls import path
from .views import LeadViewSet, FilteredLeadViewSet, MyLeadViewSet

urlpatterns = [
    path('create/', LeadViewSet.as_view({'post': 'create'})),
    path('<int:lead_id>/', LeadViewSet.as_view({'put': 'update', 'delete': 'delete'})),
    path('filter/', FilteredLeadViewSet.as_view({'get': 'list'})),
    path('filter/status/', FilteredLeadViewSet.as_view({'post': 'check_status'})),
    path('admin_dash/', MyLeadViewSet.as_view({"get": "my_leads"})),
]

"""
/filter - all/status/admin/..filter by fields
/lead/:id - CRUD
/lead/:id/comment - Create
/student/:id - CRUD
/student/:id/upload - Upload Check File


"""

