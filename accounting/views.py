from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .utils import check_paginator_data, outcome_data

from core.custom_pagination import CustomPagination
from core.BasePermissions import is_super_admin_or_hr, is_from_accounting_department, \
    is_accountant_or_super_admin, is_from_student_department

from exceptions.exception import CustomApiException
from exceptions.error_codes import ErrorCodes
from authentication.models import User
from .models import Check, OutcomeType, Outcome, ExpenditureStaff
from .serializers import (CheckSerializer, OutcomeTypeSerializer, OutcomeSerializer, OutcomeFilterSerializer,
                          ExpenditureStaffSerializer, CheckFilterSerializer, AdminCheckFilterSerializer)
from .dtos.requests import (CheckRequestSerializer, OutcomeTypeRequestSerializer, OutcomeRequestSerializer,
                            OutcomeTypeRequestUpdateSerializer, ExpenditureStaffRequestSerializer,
                            ExpenditureStaffRequestUpdateSerializer, OutcomeRequestUpdateSerializer)


class CheckViewSet(ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, ]
    parser_classes = [MultiPartParser, FormParser]

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
        operation_summary='Confirm check',
        operation_description='Confirm check',
        responses={200: 'Success', 404: "Check not found"},
        tags=['Check']
    )
    @is_accountant_or_super_admin
    def confirm_check(self, request, pk=None):
        check = Check.objects.filter(id=pk, is_deleted=False, is_confirmed=False).first()

        if not check:
            raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)

        check.is_confirmed = True
        check.save()
        return Response(data={'message': 'Check successfully confirmed!', 'ok': True}, status=status.HTTP_200_OK)


class OutcomeTypeViewSet(ViewSet):
    pagination_class = CustomPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='page', in_=openapi.IN_QUERY, description='Page number', type=openapi.TYPE_INTEGER),
            openapi.Parameter(name='page_size', in_=openapi.IN_QUERY, description='Page size number',
                              type=openapi.TYPE_INTEGER)
        ],
        operation_summary='Outcome list',
        operation_description='Outcome list',
        responses={200: OutcomeTypeSerializer()},
        tags=['Outcome']
    )
    @is_super_admin_or_hr
    def list(self, request):
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 10)
        check_paginator_data(page, page_size)
        paginator = CustomPagination()
        paginator.page = page
        paginator.page_size = page_size
        queryset = OutcomeType.objects.filter(is_deleted=False)
        paginated_users = paginator.paginate_queryset(queryset, request)
        return Response(OutcomeTypeSerializer(paginated_users, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Create Outcome Type',
        operation_description='Create Outcome Type',
        request_body=OutcomeTypeRequestSerializer,
        responses={201: OutcomeTypeSerializer(), 400: "Invalid data provided"},
        tags=['Outcome']
    )
    @is_super_admin_or_hr
    def create(self, request):
        serializer = OutcomeTypeSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED.value, message=serializer.errors)
        serializer.save()
        return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Outcome Type',
        operation_description='Outcome Type Detail',
        request_body=OutcomeTypeRequestUpdateSerializer,
        responses={200: OutcomeTypeSerializer(), 400: "Invalid data provided", 404: "Outcome type not found"},
        tags=['Outcome']
    )
    @is_super_admin_or_hr
    def update(self, request, pk=None):
        instance = OutcomeType.objects.filter(id=pk, is_deleted=False).first()
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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='page', in_=openapi.IN_QUERY, description='Page number', type=openapi.TYPE_INTEGER),
            openapi.Parameter(name='page_size', in_=openapi.IN_QUERY, description='Page size number',
                              type=openapi.TYPE_INTEGER)
        ],
        operation_summary='Outcome List',
        operation_description='Lists of Outcome',
        responses={200: OutcomeSerializer(many=True)},
        tags=['Outcome']
    )
    @is_from_accounting_department
    def list(self, request):
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 10)
        check_paginator_data(page, page_size)
        paginator = CustomPagination()
        paginator.page = page
        paginator.page_size = page_size
        queryset = Outcome.objects.filter(is_deleted=False)
        paginated_users = paginator.paginate_queryset(queryset, request)
        return Response(data={'message': OutcomeSerializer(paginated_users, many=True).data, 'ok': True},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Outcome create',
        operation_description='Outcome create',
        tags=['Outcome'],
        request_body=OutcomeRequestSerializer,
        responses={201: OutcomeSerializer(), 400: "Invalid data provided"},
    )
    @is_super_admin_or_hr
    def create(self, request):
        serializer = OutcomeSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED.value, message=serializer.errors)
        serializer.save()
        inform = outcome_data(serializer.data['type'])
        return Response(data={**serializer.data, **inform, 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Outcome detail',
        operation_description='Outcome detail',
        tags=['Outcome'],
        responses={200: OutcomeSerializer(), 404: "Outcome not found"},
    )
    @is_super_admin_or_hr
    def retrieve(self, request, pk=None):
        queryset = Outcome.objects.filter(id=pk, is_deleted=False).first()
        if not queryset:
            raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)
        serializer = OutcomeSerializer(queryset)
        return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Outcome update',
        operation_description='Outcome update',
        tags=['Outcome'],
        request_body=OutcomeRequestUpdateSerializer,
        responses={200: OutcomeSerializer(), 400: "Invalid data provided", 404: "Outcome not found"}
    )
    @is_super_admin_or_hr
    def update(self, request, pk=None):
        instance = Outcome.objects.filter(id=pk, is_deleted=False).first()
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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='page', in_=openapi.IN_QUERY, description='Page number', type=openapi.TYPE_INTEGER),
            openapi.Parameter(name='page_size', in_=openapi.IN_QUERY, description='Page size number',
                              type=openapi.TYPE_INTEGER)
        ],
        operation_summary='Expenditure list',
        operation_description='Expenditure list',
        tags=['Expenditure'],
        responses={200: ExpenditureStaffSerializer(many=True)}
    )
    @is_from_accounting_department
    def list(self, request):
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 10)
        check_paginator_data(page, page_size)
        paginator = CustomPagination()
        paginator.page = page
        paginator.page_size = page_size
        queryset = ExpenditureStaff.objects.filter(is_deleted=False)
        paginated_users = paginator.paginate_queryset(queryset, request)
        return Response(data={'message': ExpenditureStaffSerializer(paginated_users, many=True).data, 'ok': True},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Expenditure create',
        operation_description='Expenditure create',
        tags=['Expenditure'],
        request_body=ExpenditureStaffRequestSerializer,
        responses={201: ExpenditureStaffSerializer(), 400: "Invalid data provided"}
    )
    @is_super_admin_or_hr
    def create(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if user.is_deleted is True:
            raise CustomApiException(error_code=ErrorCodes.USER_DOES_NOT_EXIST.value)
        serializer = ExpenditureStaffSerializer(data={'user': pk, **request.data})
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED.value, message=serializer.errors)
        serializer.save()
        return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Expenditure detail',
        operation_description='Expenditure detail',
        tags=['Expenditure'],
        responses={200: ExpenditureStaffSerializer(), 404: "ExpenditureStaff not found"}
    )
    @is_super_admin_or_hr
    def retrieve(self, request, pk=None):
        queryset = ExpenditureStaff.objects.filter(id=pk, is_deleted=False).first()
        if not queryset:
            raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)
        serializer = ExpenditureStaffSerializer(queryset)
        return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Expenditure update',
        operation_description='Expenditure update',
        tags=['Expenditure'],
        request_body=ExpenditureStaffRequestUpdateSerializer,
        responses={200: ExpenditureStaffSerializer(), 400: "Invalid data provided",
                   404: "ExpenditureStaff not found"}
    )
    @is_super_admin_or_hr
    def update(self, request, pk=None):
        instance = ExpenditureStaff.objects.filter(id=pk, is_deleted=False).first()
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
        responses={200: CheckSerializer()},
        operation_summary='Check Filter',
        operation_description='Check Filter',
        tags=['Check']

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
        operation_summary='Check Filter',
        operation_description='Check Filter',
        tags=['Check'],
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
