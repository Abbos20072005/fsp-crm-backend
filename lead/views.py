from django.core.paginator import Paginator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Lead, Student, DocumentType, StudentDocuments, Comment
from authentication.models import User
from .permissions import check_role
from .serializer import LeadCreateSerializer, LeadUpdateSerializer, LeadSerializer, \
    CommentCreateSerializer, CommentListSerializer, BulkUpdateAdminSerializer, StudentSerializer, \
    DocumentTypeSerializer, StudentDocumentSerializer, MakeStudentSerializer


class LeadViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='List of Leads',
        operation_summary='List of Leads',
        responses={200: "List of Leads"},
    )
    @check_role
    def list(self, request, leads, *args, **kwargs):
        # Serialize the leads and return the response
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Filter Leads',
        operation_summary='Filter Leads',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Full Name'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, description='Status'),
                'start_date': openapi.Schema(type=openapi.TYPE_STRING, description='Start Date'),
                'to_date': openapi.Schema(type=openapi.TYPE_STRING, description='To Date'),
                'page': openapi.Schema(type=openapi.TYPE_INTEGER, description='Page'),
                'size': openapi.Schema(type=openapi.TYPE_INTEGER, description='Size'),
            }
        ),
        responses={200: LeadSerializer, 400: 'Bad Request'},
    )
    @check_role
    def filter(self, request, leads, *args, **kwargs):
        data = request.data
        page = data.get('page', 1)
        size = data.get('size', 2)

        if not str(page).isdigit() or int(page) < 1:
            return Response(data={'error': 'page must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
        if not str(size).isdigit() or int(size) < 1:
            return Response(data={'error': 'size must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)

        if data.get('name'):
            leads = leads.filter(name__icontains=data['name'])
        if data.get('phone_number'):
            leads = leads.filter(phone=data['phone_number'])
        if data.get('status'):
            leads = leads.filter(status=data['status'])
        if data.get('start_date'):
            leads = leads.filter(created_at__gte=data['start_date'])
        if data.get('to_date'):
            leads = leads.filter(created_at__lte=data['to_date'])

        paginator = Paginator(leads, size)
        serializer = LeadSerializer(paginator.get_page(page), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    @swagger_auto_schema(
        operation_description='Update a Lead',
        operation_summary='Update a Lead',
        request_body=LeadCreateSerializer,
        responses={200: 'Lead updated'},
    )
    def update(self, request, lead_id):
        lead = Lead.objects.filter(pk=lead_id, is_deleted=False).first()
        if not lead:
            return Response(data={"message": "Lead not found", "ok": False}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        serializer = LeadUpdateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('lead_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Lead id'),

        ],
        operation_description='Delete a Lead',
        operation_summary='Delete a Lead',
        responses={200: 'Lead deleted'},
    )
    def soft_delete(self, request, lead_id):
        lead = Lead.objects.filter(pk=lead_id, is_deleted=False).first()
        if not lead:
            return Response(data={"message": "Lead not found", "ok": False}, status=status.HTTP_404_NOT_FOUND)
        lead.is_deleted = True
        lead.save(update_fields=['is_deleted'])
        return Response(data={"message": "Lead successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, description='Search query for leads by name',
                              type=openapi.TYPE_STRING),
        ],
        operation_summary='Search Leads by name',
        operation_description='Search leads by name.',
        responses={200: LeadSerializer(many=True)},
    )
    def search_lead(self, request):
        query = request.query_params.get('query', '')
        leads = Lead.objects.filter(is_deleted=False, name__icontains=query)
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='Create a Comment',
        operation_summary='Create a Comment',
        request_body=CommentCreateSerializer,
        responses={201: 'Comment created'},
    )
    def create(self, request, lead_id):
        data = request.data
        serializer = CommentCreateSerializer(data=data, context={'request': request, 'lead_id': lead_id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='List a Comments',
        operation_summary='List a Comments',
        responses={200: 'Comment list'},
    )
    def list(self, request, lead_id):
        author_id = request.user.id
        comments = Comment.objects.filter(is_deleted=False, lead_id=lead_id, author_id=author_id)
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def bulk_update_admin(self, request):
        serializer = BulkUpdateAdminSerializer(data=request.data)
        if serializer.is_valid():
            lead_ids = serializer.validated_data['lead_ids']
            new_admin_id = serializer.validated_data['new_admin_id']

            # Retrieve the new admin
            new_admin = User.objects.get(pk=new_admin_id)

            # Update the leads
            updated_count = Lead.objects.filter(id__in=lead_ids).update(admin=new_admin)

            return Response({'success': f'{updated_count} leads updated successfully'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


# TODO: must add permissons
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


class MakeStudentViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='Create a Student',
        operation_summary='Create a Student',
        request_body=MakeStudentSerializer,
        responses={201: 'Student created', },
        tags=['Student']
    )
    def create(self, request):
        data = request.data
        lead = Lead.objects.filter(id=data['lead']).first()

        if not lead:
            return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)

        student_data = {
            'full_name': lead.name,
            'phone': lead.phone,
            'address': lead.address,
            'admin': lead.admin_id,
        }

        student_data.update(data)
        serializer = MakeStudentSerializer(data=student_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
