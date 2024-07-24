from rest_framework import status
from rest_framework.response import Response


def is_super_admin(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={'error': 'Authentication credentials were not provided'},
                            status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.role == 4:
            return func(self, request, *args, **kwargs)

        return Response(data={"error": "You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)

    return wrapper


def is_super_admin_or_hr(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={'error': 'Authentication credentials were not provided'},
                            status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.role in [3, 4]:
            return func(self, request, *args, **kwargs)
        return Response(data={"error": "You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)

    return wrapper


def is_accountant_or_super_admin(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={'error': 'Authentication credentials were not provided'},
                            status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.role in [2, 4]:
            return func(self, request, *args, **kwargs)
        return Response(data={"error": "You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)

    return wrapper


def is_employee(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={'error': 'Authentication credentials were not provided'},
                            status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.role in [1, 2, 3, 4]:
            return func(self, request, *args, **kwargs)
        return Response(data={"error": "You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)

    return wrapper


def is_from_student_department(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={'error': 'Authentication credentials were not provided'},
                            status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.role in [1, 3, 4]:
            return func(self, request, *args, **kwargs)
        return Response(data={'error': 'You do not have permission to perform this action'},
                        status=status.HTTP_403_FORBIDDEN)

    return wrapper


def is_from_accounting_department(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={'error': 'Authentication credentials were not provided'},
                            status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.role in [2, 3, 4]:
            return func(self, request, *args, **kwargs)
        return Response(data={'error': 'You do not have permission to perform this action'},
                        status=status.HTTP_403_FORBIDDEN)

    return wrapper


def is_admin_or_super_admin(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={'error': 'Authentication credentials were not provided'},
                            status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.role in [1, 4]:
            return func(self, request, *args, **kwargs)
        return Response(data={'error': 'You do not have permission to perform this action'},
                        status=status.HTTP_403_FORBIDDEN)

    return wrapper
