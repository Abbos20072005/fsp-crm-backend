from exceptions.exception import CustomApiException
from exceptions.error_codes import ErrorCodes


def is_super_admin(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated is False:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)
        elif request.user.role != 4:
            raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)
        else:
            return func(self, request, *args, **kwargs)

    return wrapper


def is_super_admin_or_hr(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)
        elif request.user.role not in [3, 4]:
            raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)
        else:
            return func(self, request, *args, **kwargs)

    return wrapper


def is_accountant_or_super_admin(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated is False:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)
        elif request.user.role not in [2, 4]:
            raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)
        else:
            return func(self, request, *args, **kwargs)

    return wrapper


def is_employee(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated is False:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)
        elif request.user.role not in [1, 2, 3, 4]:
            raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)
        else:
            return func(self, request, *args, **kwargs)

    return wrapper


def is_from_student_department(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated is False:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)
        elif request.user.role not in [1, 3, 4]:
            raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)
        else:
            return func(self, request, *args, **kwargs)

    return wrapper


def is_from_accounting_department(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated is False:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)
        elif request.user.role not in [2, 3, 4]:
            raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)
        else:
            return func(self, request, *args, **kwargs)

    return wrapper


def is_admin_or_super_admin(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated is False:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)
        elif request.user.role not in [1, 4]:
            raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)
        else:
            return func(self, request, *args, **kwargs)

    return wrapper
