from django.urls import path
from .views import LeadViewSet, StudentViewSet, DocumentTypeViewSet, StudentDocumentViewSet, \
    MakeStudentViewSet, CommentViewSet, LeadStatsViewSet


urlpatterns = [
    path('create/', LeadViewSet.as_view({'post': 'create'})),
    path('list/', LeadViewSet.as_view({'get': 'list'})),
    path('filter/', LeadViewSet.as_view({'post': 'filter'})),
    path('<int:lead_id>/', LeadViewSet.as_view({'put': 'update', 'delete': 'soft_delete'})),
    path('search/', LeadViewSet.as_view({'get': 'search_lead'}), name='search_lead'),


    path('student/', StudentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('document/type/', DocumentTypeViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('student/<int:student_id>/upload/', StudentDocumentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('make-student/', MakeStudentViewSet.as_view({'post': 'create'}))

    path('admin-dash/salary/', LeadStatsViewSet.as_view({"get": "my_salary"})),
    path('admin-dash/leads/', LeadStatsViewSet.as_view({"get": "my_leads"})),
    path('admin-dash/amount/', LeadStatsViewSet.as_view({"get": "sum_leads"})),
    path('admin-dash/count/', LeadStatsViewSet.as_view({"get": "count_leads"})),
    path('<int:lead_id>/comments/', CommentViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('', CommentViewSet.as_view({'put': 'bulk_update_admin'})),
]

"""
/filter - all/status/admin/..filter by fields
/lead/:id - CRUD
/lead/:id/comment - Create
/student/:id - CRUD
/student/:id/upload - Upload Check File


"""
