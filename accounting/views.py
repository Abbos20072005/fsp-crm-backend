from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, ListCreateAPIView, UpdateAPIView
from .serializers import CheckSerializer, OutcomeTypeSerializer, OutcomeSerializer
from .models import Check, OutcomeType, Outcome
from core.custom_pagination import CustomPagination
from rest_framework.response import Response
from rest_framework import status


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

