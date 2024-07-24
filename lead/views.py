from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Lead
from .permissions import check_role
from .serializer import LeadCreateSerializer, LeadUpdateSerializer, LeadSerializer, LeadFilterSerializer


class LeadViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='Filter a Lead',
        responses={200: 'Lead filtered'},
    )
    @check_role
    def list(self, request, leads, *args, **kwargs):
        # Serialize the leads and return the response
        serializer = LeadSerializer(leads, many=True)
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
        lead = Lead.objects.filter(pk=lead_id).first()
        if not lead:
            return Response(data={"message": "Lead not found", "ok": False}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        serializer = LeadUpdateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='Delete a Lead',
        operation_summary='Delete a Lead',
        request_body=LeadCreateSerializer,
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
        query = request.GET.get('query', "")
        leads = Lead.objects.filter(is_deleted=False, name__icontains=query)
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
