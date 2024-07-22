from django.urls import path
from .views import UserViewSet

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'register', })),
    path('me/', UserViewSet.as_view({'get': 'auth_me', })),
    path('login/', UserViewSet.as_view({'post': 'login', })),
    path('logout/', UserViewSet.as_view({'post': 'logout', })),
    path('password/', UserViewSet.as_view({'put': 'change_password', })),
    path('user/<int:user_id>/',
         UserViewSet.as_view({'patch': 'update_user', 'put': 'change_user_password', 'delete': 'soft_delete'})),
]

"""
/login
/logout
/password/update
/register
/user/update
"""
