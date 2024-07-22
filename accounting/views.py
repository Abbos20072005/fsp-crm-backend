from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.custom_pagination import CustomPagination
from core.BasePermissions import is_super_admin_or_hr, is_from_money_department, is_admin

from exceptions.exception import CustomApiException
from exceptions.error_codes import ErrorCodes

from .models import Check, OutcomeType, Outcome, ExpenditureStaff
from .utils import whose_check_list, whose_check_detail, whose_student
from .serializers import (CheckSerializer, OutcomeTypeSerializer, OutcomeSerializer, OutcomeFilterSerializer,
                          ExpenditureStaffSerializer)
from .dtos.requests import (CheckRequestSerializer, OutcomeTypeRequestSerializer, OutcomeRequestSerializer,
                            CheckRequestUpdateSerializer, OutcomeTypeRequestUpdateSerializer,
                            OutcomeRequestUpdateSerializer, ExpenditureStaffRequestSerializer,
                            ExpenditureStaffRequestUpdateSerializer)


class CheckViewSet(ViewSet):
    serializer_class = CheckSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, ]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(responses={200: CheckSerializer(many=True)})
    def list(self, request):
        check = whose_check_list(request)
        serializer = self.serializer_class(check, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Student ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: CheckSerializer(many=True), 404: "Student not found"}
    )
    def student_checks(self, request, pk=None):
        student = whose_student(request, pk=pk)
        if not student:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
        queryset = Check.objects.filter(student=student, is_deleted=False).order_by('-created_at')
        if not queryset:
            return Response({'error': 'Checks not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CheckRequestSerializer,
        responses={201: CheckSerializer(), 400: "Invalid data provided"}
    )
    @is_admin
    def create(self, request):
        request.data['uploaded_by'] = self.request.user.id
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Check ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: CheckSerializer(), 404: "Check not found"}
    )
    def retrieve(self, request, pk=None):
        check = whose_check_detail(request, pk=pk)
        if not check:
            return Response({'error': 'Check not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(check)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Check ID", type=openapi.TYPE_INTEGER),
        ],
        request_body=CheckRequestUpdateSerializer,
        responses={200: CheckSerializer(), 400: "Invalid data provided", 404: "Check not found"}
    )
    def update(self, request, pk=None):
        check = whose_check_detail(request, pk=pk)
        if not check:
            return Response({'error': 'Check not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(check, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Check ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: openapi.Response('Success'), 404: "Check not found"}
    )
    def destroy(self, request, pk=None):
        check = whose_check_detail(request, pk=pk)
        if not check:
            return Response({'error': 'Check not found.'}, status=status.HTTP_404_NOT_FOUND)

        check.is_deleted = True
        check.save()
        return Response({'success': True, 'message': 'Check successfully deleted.'}, status=status.HTTP_200_OK)


class OutcomeTypeViewSet(ViewSet):
    serializer_class = OutcomeTypeSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(responses={200: OutcomeTypeSerializer(many=True)})
    @is_super_admin_or_hr
    def list(self, request):
        queryset = OutcomeType.objects.filter(is_deleted=False)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=OutcomeTypeRequestSerializer,
        responses={201: OutcomeTypeSerializer(), 400: "Invalid data provided"}
    )
    @is_super_admin_or_hr
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Outcome Type ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: OutcomeTypeSerializer(), 404: "Outcome type not found"}
    )
    @is_super_admin_or_hr
    def retrieve(self, request, pk=None):
        queryset = OutcomeType.objects.filter(pk=pk, is_deleted=False).first()
        if not queryset:
            return Response({'error': 'Outcome type not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Outcome Type ID", type=openapi.TYPE_INTEGER),
        ],
        request_body=OutcomeTypeRequestUpdateSerializer,
        responses={200: OutcomeTypeSerializer(), 400: "Invalid data provided", 404: "Outcome type not found"}
    )
    @is_super_admin_or_hr
    def update(self, request, pk=None):
        instance = OutcomeType.objects.filter(pk=pk, is_deleted=False).first()
        if not instance:
            return Response({'error': 'Outcome type not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Outcome Type ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: openapi.Response('Success'), 404: "Outcome type not found"}
    )
    @is_super_admin_or_hr
    def destroy(self, request, pk=None):
        instance = OutcomeType.objects.filter(pk=pk, is_deleted=False).first()
        if not instance:
            return Response({'error': 'Outcome type not found.'}, status=status.HTTP_404_NOT_FOUND)

        instance.is_deleted = True
        instance.save()
        return Response({'success': True, 'message': 'Outcome type successfully deleted.'}, status=status.HTTP_200_OK)


class OutcomeViewSet(ViewSet):
    serializer_class = OutcomeSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(responses={200: OutcomeSerializer(many=True)})
    @is_from_money_department
    def list(self, request):
        queryset = Outcome.objects.filter(is_deleted=False)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=OutcomeRequestSerializer,
        responses={201: OutcomeSerializer(), 400: "Invalid data provided"}
    )
    @is_super_admin_or_hr
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Outcome ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: OutcomeSerializer(), 404: "Outcome not found"}
    )
    @is_super_admin_or_hr
    def retrieve(self, request, pk=None):
        queryset = Outcome.objects.filter(pk=pk, is_deleted=False).first()
        if not queryset:
            return Response({'error': 'Outcome not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Outcome ID", type=openapi.TYPE_INTEGER),
        ],
        request_body=OutcomeRequestUpdateSerializer,
        responses={200: OutcomeSerializer(), 400: "Invalid data provided", 404: "Outcome not found"}
    )
    @is_super_admin_or_hr
    def update(self, request, pk=None):
        instance = Outcome.objects.filter(pk=pk, is_deleted=False).first()
        if not instance:
            return Response({'error': 'Outcome not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Outcome ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: openapi.Response('Success'), 404: "Outcome not found"}
    )
    @is_super_admin_or_hr
    def destroy(self, request, pk=None):
        instance = Outcome.objects.filter(pk=pk, is_deleted=False).first()
        if not instance:
            return Response({'error': 'Outcome not found.'}, status=status.HTTP_404_NOT_FOUND)

        instance.is_deleted = True
        instance.save()
        return Response({'success': True, 'message': 'Outcome successfully deleted.'}, status=status.HTTP_200_OK)


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
        return Response(data={'result': OutcomeSerializer(outcome, many=True).data, 'ok': True},
                        status=status.HTTP_200_OK)


class ExpenditureStaffViewSet(ViewSet):
    serializer_class = ExpenditureStaffSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(responses={200: ExpenditureStaffSerializer(many=True)})
    @is_from_money_department
    def list(self, request):
        queryset = ExpenditureStaff.objects.filter(is_deleted=False)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ExpenditureStaffRequestSerializer,
        responses={201: ExpenditureStaffSerializer(), 400: "Invalid data provided"}
    )
    @is_super_admin_or_hr
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="ExpenditureStaff ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: ExpenditureStaffSerializer(), 404: "ExpenditureStaff not found"}
    )
    @is_super_admin_or_hr
    def retrieve(self, request, pk=None):
        queryset = ExpenditureStaff.objects.filter(pk=pk, is_deleted=False).first()
        if not queryset:
            return Response({'error': 'ExpenditureStaff not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="ExpenditureStaff ID", type=openapi.TYPE_INTEGER),
        ],
        request_body=ExpenditureStaffRequestUpdateSerializer,
        responses={200: ExpenditureStaffSerializer(), 400: "Invalid data provided", 404: "ExpenditureStaff not found"}
    )
    @is_super_admin_or_hr
    def update(self, request, pk=None):
        instance = ExpenditureStaff.objects.filter(pk=pk, is_deleted=False).first()
        if not instance:
            return Response({'error': 'ExpenditureStaff type not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="ExpenditureStaff ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: openapi.Response('Success'), 404: "ExpenditureStaff not found"}
    )
    @is_super_admin_or_hr
    def destroy(self, request, pk=None):
        instance = ExpenditureStaff.objects.filter(pk=pk, is_deleted=False).first()
        if not instance:
            return Response({'error': 'ExpenditureStaff not found.'}, status=status.HTTP_404_NOT_FOUND)

        instance.is_deleted = True
        instance.save()
        return Response({'success': True, 'message': 'ExpenditureStaff successfully deleted.'},
                        status=status.HTTP_200_OK)
