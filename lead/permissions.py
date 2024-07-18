from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import Lead


def check_role(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'admin':
            leads = Lead.objects.filter(assigned_admin=user)
        elif user.role in ['hr', 'superadmin']:
            leads = Lead.objects.all()
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        return func(self, request, leads, *args, **kwargs)

    return wrapper
