from django.urls import path
from .views import UserViewSet

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'register', })),
    path('login/', UserViewSet.as_view({'post': 'login', })),
    path('logout/', UserViewSet.as_view({'post': 'logout', })),
    path('password/', UserViewSet.as_view({'put': 'change_password', })),
    path('user/<int:user_id>', UserViewSet.as_view({'put': 'update_user', 'patch': 'change_user_password'})),
]

"""
/login
/logout
/password/update
/register
/user/update
"""
