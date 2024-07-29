from datetime import date
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from lead.models import Student
from exceptions.exception import CustomApiException
from exceptions.error_codes import ErrorCodes
from accounting.models import Check, OutcomeType, Outcome


def whose_check_list(*args, **kwargs):
    request = args[0]
    if request.user.role == 1:
        check = Check.objects.filter(is_deleted=False, uploaded_by=request.user.id).order_by('-created_at')
        return check
    elif request.user.role in [2, 3, 4]:
        check = Check.objects.filter(is_deleted=False).order_by('-created_at')
        return check
    raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)


def whose_check_detail(*args, **kwargs):
    request = args[0]
    pk = kwargs['pk']
    if request.user.role == 1:
        check = Check.objects.filter(pk=pk, is_deleted=False, uploaded_by=request.user.id).first()
        return check
    elif request.user.role in [2, 3, 4]:
        check = Check.objects.filter(is_deleted=False).first()
        return check
    raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)


def whose_student(*args, **kwargs):
    pk = kwargs['pk']
    request = args[0]
    if request.user.role in [2, 3, 4]:
        student = Student.objects.filter(is_deleted=False).first()
        return student
    elif request.user.role == 1:
        student = Student.objects.filter(pk=pk, is_deleted=False, lead__admin_id=request.user.id).first()
        return student
    raise CustomApiException(error_code=ErrorCodes.FORBIDDEN.value)


def check_paginator_data(page, page_size):
    if not str(page).isnumeric() or not str(page_size).isnumeric():
        raise ValidationError('Page and Page size should be positive integer number')


def outcome_data(out_type) -> dict:
    today = date.today()
    outcome_type = OutcomeType.objects.filter(is_deleted=False, id=out_type).first()
    outcome_type_percent = outcome_type.limit
    check = Check.objects.filter(created_at__year=today.year, created_at__month=today.month, is_confirmed=True,
                                 is_deleted=False).order_by('created_at')
    confirmed = float(check.values('amount').distinct().aggregate(total_amount=Sum('amount'))['total_amount']) or 0
    limit_amount = confirmed * outcome_type_percent / 100
    outcome = Outcome.objects.filter(created_at__year=today.year, created_at__month=today.month, is_deleted=False,
                                     type=outcome_type).order_by('created_at')
    outcome_amount = float(
        outcome.values('amount').distinct().aggregate(total_amount=Sum('amount'))['total_amount']) or 0
    return {
        'limit': limit_amount,
        'used': outcome_amount,
        'usable': limit_amount - outcome_amount
    }
