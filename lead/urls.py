from django.urls import path
from .views import LeadViewSet, LeadListViewSet, FilteredLeadViewSet

urlpatterns = [
    path('create/', LeadViewSet.as_view({'post': 'create'})),
    path('<int:lead_id>/', LeadViewSet.as_view({'put': 'update', 'delete': 'delete'})),
    path('list/leads', LeadListViewSet.as_view({'get': 'list'})),

    path('filter/', FilteredLeadViewSet.as_view({'post': 'check_status', 'get': 'filter_lead'})),

]

"""
/filter - all/status/admin/..filter by fields
/lead/:id - CRUD
/lead/:id/comment - Create
/student/:id - CRUD
/student/:id/upload - Upload Check File


"""

