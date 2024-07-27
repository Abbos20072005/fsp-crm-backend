from django.urls import path
from .views import LeadViewSet, StudentViewSet, DocumentTypeViewSet, StudentDocumentViewSet, \
    MakeStudentViewSet
from .views import LeadViewSet, CommentViewSet

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
]

"""
/filter - all/status/admin/..filter by fields
/lead/:id - CRUD
/lead/:id/comment - Create
/student/:id - CRUD
/student/:id/upload - Upload Check File


"""
