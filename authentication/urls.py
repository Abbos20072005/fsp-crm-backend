from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserViewSet, UserDetailView

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'register', })),
    path('me/', UserViewSet.as_view({'get': 'auth_me', })),
    path('login/', UserViewSet.as_view({'post': 'login', })),
    path('logout/', UserViewSet.as_view({'post': 'logout', })),
    path('password/', UserViewSet.as_view({'put': 'change_password', })),
    path('users/<int:user_id>/',
         UserViewSet.as_view({'patch': 'update_user', 'put': 'change_user_password', 'delete': 'soft_delete'})),
    path('users/filter/', UserViewSet.as_view({'post': 'filter_users', })),
    path('users/search/', UserViewSet.as_view({'get': 'search_user'}), name='search_user'),
    path('user-details/', UserDetailView.as_view({
        'patch': 'update'
    }), name='user-details'),
]

"""
/login
/logout
/password/update
/register
/user/update
"""
