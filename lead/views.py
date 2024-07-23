from django.core.paginator import Paginator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Lead
from .permissions import check_role
from .serializer import LeadCreateSerializer, LeadUpdateSerializer, LeadSerializer, CommentSerializer


class LeadViewSet(ViewSet):
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
        size = data.get('size', 10)
        if not str(page).isdigit() or int(page) < 1:
            return Response(data={'error': 'page must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
        if not str(size).isdigit() or int(size) < 1:
            return Response(data={'error': 'size must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)

        if data.get('name'):
            leads = leads.filter(name__icontains=data['name'])
        if data.get('phone_number'):
            leads = leads.filter(phone=data['phone_number'])
        if data.get('status') and data['status'] in [1, 2, 4]:
            leads = leads.filter(status=data['status'])
        if data.get('start_date'):
            leads = leads.filter(created_at__gte=data['start_date'])
        if data.get('to_date'):
            leads = leads.filter(created_at__lte=data['to_date'])
        paginator = Paginator(leads, size)
        serializer = LeadSerializer(paginator.page(page), many=True)
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
