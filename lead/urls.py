from django.urls import path
from .views import LeadViewSet, StudentViewSet, DocumentTypeViewSet, StudentDocumentViewSet

urlpatterns = [
    path('create/', LeadViewSet.as_view({'post': 'create'})),
    path('<int:lead_id>/', LeadViewSet.as_view({'put': 'update', 'delete': 'delete'})),
    path('filter/', LeadViewSet.as_view({'post': 'filter'})),
    path('student/', StudentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('document/type/', DocumentTypeViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('documents/', StudentDocumentViewSet.as_view({'get': 'list', 'post': 'create'})),
]

"""
/filter - all/status/admin/..filter by fields
/lead/:id - CRUD
/lead/:id/comment - Create
/student/:id - CRUD
/student/:id/upload - Upload Check File


"""
