from django.urls import path
from .views import LeadViewSet, FilteredLeadViewSet, StudentViewSet, DocumentTypeViewSet, StudentDocumentViewSet, \
    MakeStudentViewSet
from .views import LeadViewSet, CommentViewSet

urlpatterns = [
    path('create/', LeadViewSet.as_view({'post': 'create'})),
    path('list/', LeadViewSet.as_view({'get': 'list'})),
    path('filter/', LeadViewSet.as_view({'post': 'filter'})),
    path('<int:lead_id>/', LeadViewSet.as_view({'put': 'update', 'delete': 'soft_delete'})),
    path('search/', LeadViewSet.as_view({'get': 'search_lead'}), name='search_lead'),

    path('<int:lead_id>/comments/', CommentViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('', CommentViewSet.as_view({'put': 'bulk_update_admin'})),
    path('<int:lead_id>/', LeadViewSet.as_view({'put': 'update', 'delete': 'delete'})),
    path('filter/', FilteredLeadViewSet.as_view({'get': 'list'})),
    path('filter/status/', FilteredLeadViewSet.as_view({'post': 'check_status'})),
    path('student/', StudentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('document/type/', DocumentTypeViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('student/<int:student_id>/upload/', StudentDocumentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('make-student/', MakeStudentViewSet.as_view({'post': 'create'}))
]

"""
/filter - all/status/admin/..filter by fields
/lead/:id - CRUD
/lead/:id/comment - Create
/student/:id - CRUD
/student/:id/upload - Upload Check File


"""

