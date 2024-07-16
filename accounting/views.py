from django.db.models import Q
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, ListCreateAPIView, UpdateAPIView
from .serializers import CheckSerializer, OutcomeTypeSerializer, OutcomeSerializer
from .models import Check, OutcomeType, Outcome
from core.custom_pagination import CustomPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import OutcomeFilterSerializer


class CheckRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = CheckSerializer
    queryset = Check.objects.filter(is_deleted=False)


class CheckListAPIView(ListAPIView):
    serializer_class = CheckSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Check.objects.filter(is_deleted=False).order_by('-created_at')


class CheckStudentListAPIView(ListAPIView):
    def list(self, request, *args, **kwargs):
        student_id = self.kwargs['pk']
        checks = Check.objects.filter(student_id=student_id, is_deleted=False)
        serializer = CheckSerializer(checks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OutcomeTypeListCreateAPIView(ListCreateAPIView):
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        outcome_type = OutcomeType.objects.filter(is_deleted=False)
        serializer = OutcomeTypeSerializer(outcome_type, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = OutcomeTypeSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OutcomeTypeRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = OutcomeTypeSerializer
    queryset = OutcomeType.objects.filter(is_deleted=False)


class OutcomeTypeDestroy(UpdateAPIView):
    queryset = OutcomeType.objects.filter(is_deleted=False)
    serializer_class = OutcomeTypeSerializer
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if not self.get_object().is_deleted:
            instance.is_deleted = True
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        data = {
            'success': True,
            'message': 'Outcome type successfully deleted.',
        }
        return Response(data, status=status.HTTP_200_OK)


class CheckDestroy(UpdateAPIView):
    queryset = Check.objects.filter(is_deleted=False)
    serializer_class = CheckSerializer
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_deleted:
            instance.is_deleted = True
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        data = {
            'success': True,
            'message': 'Check successfully deleted.',
        }
        return Response(data, status=status.HTTP_200_OK)


class OutcomeListCreateAPIView(ListCreateAPIView):
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        outcome = Outcome.objects.filter(is_deleted=False)
        serializer = OutcomeSerializer(outcome, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = OutcomeSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserSalaryListAPIView(ListAPIView):
    pagination_class = CustomPagination


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
            return Response(data={'error': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        types = request.query_params.get('type')
        time_from = request.query_params.get('time_from')
        time_to = request.query_params.get('time_to')

        outcome = Outcome.objects.filter(Q(type=types) | Q(created_at__gte=time_from, created_at__lte=time_to))
        return Response(data={'result': OutcomeSerializer(outcome, many=True).data, 'ok': True},
                        status=status.HTTP_200_OK)
