from drf_yasg.utils import swagger_auto_schema

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Lead, Student, DocumentType, StudentDocuments
from .permissions import check_role
from .serializer import LeadCreateSerializer, LeadUpdateSerializer, LeadSerializer, CommentSerializer, \
    LeadStatusSerializer, StudentSerializer, DocumentTypeSerializer, StudentDocumentSerializer


class LeadViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='Create a Lead',
        operation_summary='Create a Lead',
        request_body=LeadCreateSerializer,
        responses={201: 'Lead created'},
    )
    def create(self, request):
        data = request.data
        serializer = LeadCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, lead_id):
        lead = Lead.objects.filter(pk=lead_id).first()
        if not lead:
            return Response(data={"message": "Lead not found", "ok": False}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        serializer = LeadUpdateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, lead_id):
        lead = Lead.objects.filter(pk=lead_id).first()
        if not lead:
            return Response(data={"message": "Lead not found", "ok": False}, status=status.HTTP_404_NOT_FOUND)
        lead.is_deleted = True
        lead.save(update_fields=['is_deleted'])
        return Response(data={"message": "Lead successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


class FilteredLeadViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='Filter a Lead',
        responses={200: 'Lead filtered'},
    )
    @check_role
    def list(self, request, leads, *args, **kwargs):
        # Serialize the leads and return the response
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def check_status(self, request):
        data = request.data
        serializer = LeadStatusSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer.validated_data['status'] == 1:
            leads = Lead.objects.filter(status=1)
        elif serializer.validated_data['status'] == 2:
            leads = Lead.objects.filter(status=2)
        elif serializer.validated_data['status'] == 4:
            leads = Lead.objects.filter(status=4)
        else:
            return Response(data={'error': 'Status not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DocumentTypeViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='Create a Document Type',
        operation_summary='Create a Student',
        request_body=DocumentTypeSerializer,
        responses={201: 'Document Type created', },
        tags=['Documents']
    )
    def create(self, request):
        serializer = DocumentTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='Remove and get document type',
        responses={200: 'Document type'},
        tags=['Documents'],

    )
    def list(self, request):
        queryset = DocumentType.objects.all()
        serializer = DocumentTypeSerializer(queryset, many=True)
        if not serializer.data:
            return Response(serializer.errors, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentDocumentViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='Create a Document',
        operation_summary='Create a Document',
        request_body=StudentDocumentSerializer,
        responses={201: 'Document created', },
        tags=['Documents']
    )
    def create(self, request, student_id):
        data = request.data
        data['student'] = Student.objects.filter(id=student_id).first()
        print(data)
        serializer = StudentDocumentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='get student documents',
        responses={200: 'Documents'},
        tags=['Documents'],

    )
    def list(self, request):
        queryset = Student.objects.all()
        serializer = StudentSerializer(queryset, many=True)
        if not serializer.data:
            return Response(serializer.errors, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='Create a Student',
        operation_summary='Create a Student',
        request_body=StudentSerializer,
        responses={201: 'Student created', },
        tags=['Student']
    )
    def create(self, request):
        data = request.data
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='Remove and get student documents',
        responses={200: 'Student documents'},
        tags=['Student']
    )
    def list(self, request):
        queryset = Student.objects.all()
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
