from .models import Check
from lead.models import Student
from .exceptions import BadRequestException


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

