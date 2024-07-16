from django.urls import path
from .views import UserViewSet

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'register', })),
    path('login/', UserViewSet.as_view({'post': 'login', })),
    path('logut/', UserViewSet.as_view({'post': 'logout', })),
    path('password/', UserViewSet.as_view({'put': 'change_password', })),
]

"""
/login
/logout
/password/update
/register
/user/update
"""
