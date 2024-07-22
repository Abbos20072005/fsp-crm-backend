from rest_framework import status
from rest_framework.response import Response


def is_super_admin(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 4:
            return func(self, request, *args, **kwargs)

        return Response(data={"error": "You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)

    return wrapper


def is_super_admin_or_hr(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in [3, 4]:
            return func(self, request, *args, **kwargs)
        return Response(data={"error": "You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)

    return wrapper


def is_accountant_or_super_admin(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in [2, 4]:
            return func(self, request, *args, **kwargs)
        return Response(data={"error": "You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)

    return wrapper


def is_employee(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in [1, 2, 3, 4]:
            return func(self, request, *args, **kwargs)
        return Response(data={"error": "You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)

    return wrapper


def is_from_student_department(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in [1, 3, 4]:
            return func(self, request, *args, **kwargs)
        return Response(data={'error': 'You do not have permission to perform this action'},
                        status=status.HTTP_403_FORBIDDEN)

    return wrapper


def is_from_money_department(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in [2, 3, 4]:
            return func(self, request, *args, **kwargs)
        return Response(data={'error': 'You do not have permission to perform this action'},
                        status=status.HTTP_403_FORBIDDEN)

    return wrapper


def is_admin_or_super_admin(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in [1, 4]:
            return func(self, request, *args, **kwargs)
        return Response(data={'error': 'You do not have permission to perform this action'},
                        status=status.HTTP_403_FORBIDDEN)

    return wrapper
