from rest_framework import status
from rest_framework.response import Response

from exceptions.error_codes import ErrorCodes
from exceptions.exception import CustomApiException


def is_super_admin(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)
        elif request.user.role == 4:
            return func(self, request, *args, **kwargs)

        raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)

    return wrapper


def is_super_admin_or_hr(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)
        elif request.user.role in [3, 4]:
            return func(self, request, *args, **kwargs)
        raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)

    return wrapper


def is_accountant_or_super_admin(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)
        elif request.user.role in [2, 4]:
            return func(self, request, *args, **kwargs)
        raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)

    return wrapper


def is_employee(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)
        elif request.user.role in [1, 2, 3, 4]:
            return func(self, request, *args, **kwargs)
        raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)

    return wrapper


def is_from_student_department(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)
        elif request.user.role in [1, 3, 4]:
            return func(self, request, *args, **kwargs)
        raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)

    return wrapper


def is_from_accounting_department(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)
        elif request.user.role in [2, 3, 4]:
            return func(self, request, *args, **kwargs)
        raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)

    return wrapper


def is_admin_or_super_admin(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)
        elif request.user.role in [1, 4]:
            return func(self, request, *args, **kwargs)
        raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)

    return wrapper
