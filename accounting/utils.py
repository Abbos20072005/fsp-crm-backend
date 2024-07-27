from datetime import date
from django.db.models import Sum
from authentication.models import User

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


# def calculate_salary_of_admin(admin_id: int) -> dict:
#     admin = User.objects.filter(id=admin_id, is_deleted=False).first()
#     today = date.today()
#     kpi_from_check = Check.objects.filter(uploaded_by=admin_id, created_at__year=today.year,
#                                           created_at__month=today.month).count()
#     expenditure = ExpenditureStaff.objects.filter(user_id=admin_id, is_deleted=False).order_by('-created_at')
#     minus = expenditure.values('amount').distinct().aggregate(total_amount=Sum('amount'))['total_amount'] or 0
#     data = {
#         'student_quantity': kpi_from_check,
#         'kpi_amount': kpi_from_check * admin.kpi,
#         "fixed_salary": admin.fixed_salary,
#         'fine': minus,
#         'total': kpi_from_check * admin.kpi + admin.fixed_salary - minus
#     }
#     return data
#
#
# def calculate_confirmed_check(type) -> dict:
#     today = date.today()
#     outcome_type = OutcomeType.objects.filter(is_deleted=False, name=type).first()
#     outcome_type_percent = outcome_type.values('type')
#     check = Check.objects.filter(created_at__year=today.year, created_at__month=today.month, is_confirmed=True,
#                                  is_deleted=False).order_by('created_at')
#     confirmed = check.values('amount').distinct().aggregate(total_amount=Sum('amount'))['total_amount']
#     limit_amount = confirmed * outcome_type_percent / 100
#     outcome = Outcome.objects.filter(created_at__year=today.year, created_at__month=today.month, is_deleted=False,
#                                      type=outcome_type).first()
#     outcome_amount = outcome.values('amount').distinct().aggregate(total_amount=Sum('amount'))['total_amount']
#     return {
#             'limit': limit_amount,
#             'used': outcome_amount,
#             'usable': limit_amount - outcome_amount
#             }
