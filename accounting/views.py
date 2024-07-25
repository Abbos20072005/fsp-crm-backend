from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.custom_pagination import CustomPagination
from core.BasePermissions import is_super_admin_or_hr, is_from_accounting_department, is_admin_or_super_admin, \
    is_accountant_or_super_admin, is_from_student_department

from exceptions.exception import CustomApiException
from exceptions.error_codes import ErrorCodes

from .models import Check, OutcomeType, Outcome, ExpenditureStaff
from .utils import whose_check_list, whose_check_detail, whose_student, calculate_confirmed_check, \
    calculate_salary_of_admin
from .serializers import (CheckSerializer, OutcomeTypeSerializer, OutcomeSerializer, OutcomeFilterSerializer,
                          ExpenditureStaffSerializer, CheckFilterSerializer, AdminCheckFilterSerializer)
from .dtos.requests import (CheckRequestSerializer, OutcomeTypeRequestSerializer, OutcomeRequestSerializer,
                            CheckRequestUpdateSerializer, OutcomeTypeRequestUpdateSerializer,
                            OutcomeRequestUpdateSerializer, ExpenditureStaffRequestSerializer,
                            ExpenditureStaffRequestUpdateSerializer)


# TODO:filter for checks
class CheckViewSet(ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, ]
    parser_classes = [MultiPartParser, FormParser]

    # @swagger_auto_schema(
    #     operation_summary='Checks list for accountant',
    #     operation_description='Checks list for accountant for confirmation',
    #     responses={200: CheckSerializer(many=True)},
    #     tags=['Check']
    # )
    # def list(self, request):
    #     check = whose_check_list(request)
    #     serializer = CheckSerializer(check, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Create check',
        operation_description='Create check',
        request_body=CheckRequestSerializer,
        responses={201: CheckSerializer(), 400: "Invalid data provided"},
        tags=['Check']
    )
    @is_from_student_department
    def create(self, request):
        request.data['uploaded_by'] = request.user.id
        serializer = CheckSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED.value, message=serializer.errors)
        serializer.save()
        return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('check_id', openapi.IN_PATH, description="Check ID", type=openapi.TYPE_INTEGER),
        ],
        operation_summary='Confirm check',
        operation_description='Confirm check',
        responses={200: openapi.Response('Success'), 404: "Check not found"},
        tags=['Check']
    )
    @is_accountant_or_super_admin
    def confirm_check(self, request, check_id=None):
        check = Check.objects.filter(id=check_id, is_deleted=False, is_confirmed=False).first()
        if not check:
            raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)

        check.is_confirmed = True
        check.save()
        return Response(data={'message': 'Check successfully confirmed.', 'ok': True}, status=status.HTTP_200_OK)


class OutcomeTypeViewSet(ViewSet):
    pagination_class = CustomPagination

    @swagger_auto_schema(responses={200: OutcomeTypeSerializer(many=True)})
    @is_super_admin_or_hr
    def list(self, request):
        queryset = OutcomeType.objects.filter(is_deleted=False)
        serializer = OutcomeTypeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=OutcomeTypeRequestSerializer,
        responses={201: OutcomeTypeSerializer(), 400: "Invalid data provided"}
    )
    @is_super_admin_or_hr
    def create(self, request):
        serializer = OutcomeTypeSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED.value, message=serializer.errors)
        serializer.save()
        return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('outcome_type_id', openapi.IN_PATH, description="Outcome Type ID",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={200: OutcomeTypeSerializer(), 404: "Outcome type not found"}
    )
    @is_super_admin_or_hr
    def retrieve(self, request, outcome_type_id=None):
        queryset = OutcomeType.objects.filter(pk=outcome_type_id, is_deleted=False).first()
        if not queryset:
            raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)
        serializer = OutcomeTypeSerializer(queryset)
        return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

        @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter('outcome_type_id', openapi.IN_PATH, description="Outcome Type ID",
                                  type=openapi.TYPE_INTEGER),
            ],
            request_body=OutcomeTypeRequestUpdateSerializer,
            responses={200: OutcomeTypeSerializer(), 400: "Invalid data provided", 404: "Outcome type not found"}
        )
        @is_super_admin_or_hr
        def update(self, request, outcome_type_id=None):
            instance = OutcomeType.objects.filter(pk=outcome_type_id, is_deleted=False).first()
            if not instance:
                raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)

            serializer = OutcomeTypeSerializer(instance, data=request.data, partial=True)
            if not serializer.is_valid():
                raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED.value, message=serializer.errors)
            serializer.save()
            return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    class OutcomeViewSet(ViewSet):
        pagination_class = CustomPagination
        permission_classes = [IsAuthenticated, ]

        @swagger_auto_schema(responses={200: OutcomeSerializer(many=True)})
        @is_from_accounting_department
        def list(self, request):
            queryset = Outcome.objects.filter(is_deleted=False)
            serializer = OutcomeSerializer(queryset, many=True)
            return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

        @swagger_auto_schema(
            request_body=OutcomeRequestSerializer,
            responses={201: OutcomeSerializer(), 400: "Invalid data provided"}
        )
        @is_super_admin_or_hr
        def create(self, request):
            serializer = OutcomeSerializer(data=request.data)
            if not serializer.is_valid():
                raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED.value, message=serializer.errors)
            serializer.save()
            return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

        @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter('outcome_id', openapi.IN_PATH, description="Outcome ID", type=openapi.TYPE_INTEGER),
            ],
            responses={200: OutcomeSerializer(), 404: "Outcome not found"},
            tags=['Accounting']
        )
        @is_super_admin_or_hr
        def retrieve(self, request, outcome_id=None):
            queryset = Outcome.objects.filter(pk=outcome_id, is_deleted=False).first()
            if not queryset:
                raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)
            serializer = OutcomeSerializer(queryset)
            return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

        @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter('pk', openapi.IN_PATH, description="Outcome ID", type=openapi.TYPE_INTEGER),
            ],
            request_body=OutcomeRequestUpdateSerializer,
            responses={200: OutcomeSerializer(), 400: "Invalid data provided", 404: "Outcome not found"}
        )
        @is_super_admin_or_hr
        def update(self, request, outcome_id=None):
            instance = Outcome.objects.filter(pk=outcome_id, is_deleted=False).first()
            if not instance:
                raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)

            serializer = OutcomeSerializer(instance, data=request.data, partial=True)
            if not serializer.is_valid():
                raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED.value, message=serializer.errors)
            serializer.save()
            return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    class OutcomeFilterViewSet(ViewSet):
        @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter('type', openapi.IN_QUERY, description='Outcome Type', type=openapi.TYPE_INTEGER),
                openapi.Parameter('time_from', openapi.IN_QUERY, description='Start time', type=openapi.TYPE_STRING),
                openapi.Parameter('time_to', openapi.IN_QUERY, description='End time', type=openapi.TYPE_STRING),
            ],
            operation_summary='Outcome Filter',
            operation_description='Outcome Filter',
            responses={200: OutcomeSerializer()},
            tags=['Outcome']
        )
        def outcome_filter(self, request):
            serializer = OutcomeFilterSerializer(data=request.query_params)

            if not serializer.is_valid():
                raise CustomApiException(ErrorCodes.VALIDATION_FAILED.value, message=serializer.errors)

            types = request.query_params.get('type')
            time_from = request.query_params.get('time_from')
            time_to = request.query_params.get('time_to')

            result = {}
            if types:
                result['type'] = types
            if time_from and time_to:
                result['created_at__gte'] = time_from
                result['created_at__lte'] = time_to

            outcome = Outcome.objects.filter(**result)
            return Response(data={'message': OutcomeSerializer(outcome, many=True).data, 'ok': True},
                            status=status.HTTP_200_OK)

    class ExpenditureStaffViewSet(ViewSet):
        pagination_class = CustomPagination
        permission_classes = [IsAuthenticated, ]

        @swagger_auto_schema(responses={200: ExpenditureStaffSerializer(many=True)})
        @is_from_accounting_department
        def list(self, request):
            queryset = ExpenditureStaff.objects.filter(is_deleted=False)
            serializer = ExpenditureStaffSerializer(queryset, many=True)
            return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

        @swagger_auto_schema(
            request_body=ExpenditureStaffRequestSerializer,
            responses={201: ExpenditureStaffSerializer(), 400: "Invalid data provided"}
        )
        @is_super_admin_or_hr
        def create(self, request):
            user = ExpenditureStaff.objects.filter(user=request.user.id).first()
            if user.is_deleted is True:
                raise CustomApiException(error_code=ErrorCodes.USER_DOES_NOT_EXIST.value)
            serializer = ExpenditureStaffSerializer(data=request.data)
            if not serializer.is_valid():
                raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED.value, message=serializer.errors)
            serializer.save()
            return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

        @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter('expenditure_staff_id', openapi.IN_PATH, description="ExpenditureStaff ID",
                                  type=openapi.TYPE_INTEGER),
            ],
            responses={200: ExpenditureStaffSerializer(), 404: "ExpenditureStaff not found"}
        )
        @is_super_admin_or_hr
        def retrieve(self, request, expenditure_staff_id=None):
            queryset = ExpenditureStaff.objects.filter(pk=expenditure_staff_id, is_deleted=False).first()
            if not queryset:
                raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)
            serializer = ExpenditureStaffSerializer(queryset)
            return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

        @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter('expenditure_staff_id', openapi.IN_PATH, description="ExpenditureStaff ID",
                                  type=openapi.TYPE_INTEGER),
            ],
            request_body=ExpenditureStaffRequestUpdateSerializer,
            responses={200: ExpenditureStaffSerializer(), 400: "Invalid data provided",
                       404: "ExpenditureStaff not found"}
        )
        @is_super_admin_or_hr
        def update(self, request, expenditure_staff_id=None):
            instance = ExpenditureStaff.objects.filter(pk=expenditure_staff_id, is_deleted=False).first()
            if not instance:
                raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)

            serializer = ExpenditureStaffSerializer(instance, data=request.data, partial=True)
            if not serializer.is_valid():
                raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED.value, message=serializer.errors)
            serializer.save()
            return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    class CheckFilterViewSet(ViewSet):
        @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter('time_from', openapi.IN_QUERY, description='Start time', type=openapi.TYPE_STRING),
                openapi.Parameter('time_to', openapi.IN_QUERY, description='End time', type=openapi.TYPE_STRING),
            ],
            operation_summary='Check Filter',
            operation_description='Check Filter',
            responses={200: CheckSerializer()}
        )
        @is_accountant_or_super_admin
        def check_filter(self, request):
            serializer = CheckFilterSerializer(data=request.query_params)
            if not serializer.is_valid():
                raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED.value, message=serializer.errors)
            time_from = request.query_params.get('time_from')
            time_to = request.query_params.get('time_to')
            result = {}
            if time_from and time_to:
                result['created_at__gte'] = time_from
                result['created_at__lte'] = time_to

            check = Check.objects.filter(**result)
            data = CheckSerializer(check, many=True).data
            return Response(data={'message': data, 'ok': True}, status=status.HTTP_200_OK)

    class AdminCheckFilterViewSet(ViewSet):
        @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter('uploaded_by', openapi.IN_QUERY, description='Admin ID', type=openapi.TYPE_INTEGER),
                openapi.Parameter('time_from', openapi.IN_QUERY, description='Start time', type=openapi.TYPE_STRING),
                openapi.Parameter('time_to', openapi.IN_QUERY, description='End time', type=openapi.TYPE_STRING),
            ],
            responses={200: CheckSerializer()},
        )
        @is_accountant_or_super_admin
        def check_by_admin_filter(self, request):
            serializer = AdminCheckFilterSerializer(data=request.query_params)
            if not serializer.is_valid():
                raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED.value, message=serializer.errors)
            admin = request.query_params.get('uploaded_by')
            time_from = request.query_params.get('time_from')
            time_to = request.query_params.get('time_to')

            result = {}
            if admin:
                result['uploaded_by'] = admin
            if time_from and time_to:
                result['created_at__gte'] = time_from
                result['created_at__lte'] = time_to

            check = Check.objects.filter(**result)
            data = CheckSerializer(check, many=True).data
            return Response(data={'message': data, 'ok': True}, status=status.HTTP_200_OK)

    class AdminSalaryViewSet(ViewSet):
        @is_accountant_or_super_admin
        def get_salary(self, request, pk=None):
            data = calculate_salary_of_admin(pk)
            if not data:
                raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)
            return Response(data, status=status.HTTP_200_OK)

    class CheckAmountViewSet(ViewSet):

        @is_accountant_or_super_admin
        def get_check(self, request):
            amount = calculate_confirmed_check()
            if not amount:
                raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)
            data = {
                'Check amount for this month': amount
            }
            return Response(data, status=status.HTTP_200_OK)
