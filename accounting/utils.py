from datetime import date

from lead.models import Student
from .exceptions import BadRequestException
from django.db.models import Sum
from authentication.models import User
from accounting.models import Check, ExpenditureStaff, OutcomeType


def whose_check_list(*args, **kwargs):
    request = args[0]
    if request.user.role == 1:
        check = Check.objects.filter(is_deleted=False, uploaded_by=request.user.id).order_by('-created_at')
        return check
    elif request.user.role in [2, 3, 4]:
        check = Check.objects.filter(is_deleted=False).order_by('-created_at')
        return check
    raise BadRequestException('You have not access to see checks')


def whose_check_detail(*args, **kwargs):
    request = args[0]
    pk = kwargs['pk']
    if request.user.role == 1:
        check = Check.objects.filter(pk=pk, is_deleted=False, uploaded_by=request.user.id).first()
        return check
    elif request.user.role in [2, 3, 4]:
        check = Check.objects.filter(is_deleted=False).first()
        return check
    raise BadRequestException("You have not access to see this check")


def whose_student(*args, **kwargs):
    pk = kwargs['pk']
    request = args[0]
    if request.user.role in [2, 3, 4]:
        student = Student.objects.filter(is_deleted=False).first()
        return student
    elif request.user.role == 1:
        student = Student.objects.filter(pk=pk, is_deleted=False, lead__admin_id=request.user.id).first()
        return student
    raise BadRequestException("You have not access to see this student's checks")


def calculate_salary_of_admin(admin_id: int) -> dict:
    admin = User.objects.filter(id=admin_id, is_deleted=False).first()
    today = date.today()
    kpi_from_check = Check.objects.filter(uploaded_by=admin_id, created_at__year=today.year,
                                          created_at__month=today.month).count()
    expenditure = ExpenditureStaff.objects.filter(user_id=admin_id, is_deleted=False).order_by('-created_at')
    minus = expenditure.values('amount').distinct().aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    data = {
        'Student quantity': kpi_from_check,
        'KPI amount': kpi_from_check * admin.kpi,
        "Admin's fixed salary": admin.fixed_salary,
        'Fine for Admin': minus,
        'Total salary for this month': kpi_from_check * admin.kpi + admin.fixed_salary - minus
    }
    return data


def calculate_confirmed_check() -> float:
    today = date.today()
    check = Check.objects.filter(created_at__year=today.year, created_at__month=today.month, is_confirmed=True,
                                 is_deleted=False).order_by('created_at')
    return check.values('amount').distinct().aggregate(total_amount=Sum('amount'))['total_amount'] or 0


