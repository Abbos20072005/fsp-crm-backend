from rest_framework.response import Response
from rest_framework import status
from .models import Lead
from .serializer import LeadStatusSerializer


def check_role(func):
    def wrapper(self, request, *args, **kwargs):

        if request.user.is_authenticated and request.user.role == 1:
            leads = Lead.objects.filter(admin=request.user)
        elif request.user.is_authenticated and request.user.role in [3, 4]:
            leads = Lead.objects.all()
        else:
            return Response(data={'error': 'You dont have permissions to perform this action'},
                            status=status.HTTP_403_FORBIDDEN)

        return func(self, request, leads, *args, **kwargs)

    return wrapper



