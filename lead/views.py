from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Lead
from .permissions import check_role
from .serializer import LeadCreateSerializer, LeadUpdateSerializer, LeadSerializer, LeadStatusSerializer, \
    LeadFilterSerializer


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
    def delete(self, request, lead_id):
        lead = Lead.objects.filter(pk=lead_id).first()
        if not lead:
            return Response(data={"message": "Lead not found", "ok": False}, status=status.HTTP_404_NOT_FOUND)
        lead.is_deleted = True
        lead.save(update_fields=['is_deleted'])
        return Response(data={"message": "Lead successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


class LeadListViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='Filter a Lead',
        responses={200: 'Lead filtered'},
    )
    @check_role
    def list(self, request, leads, *args, **kwargs):
        # Serialize the leads and return the response
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FilteredLeadViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='Status lead',
        responses={200: 'Lead status lead',
                   404: 'Status not found'},
        request_body=LeadStatusSerializer,
    )
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

    queryset = Lead.objects.all()
    serializer_class = LeadFilterSerializer

    @swagger_auto_schema(
        operation_description='Filter a Lead',
        responses={200: 'Lead filtered'},
    )
    @action(detail=False, methods=['get'])
    def filter_lead(self, request):
        name = request.query_params.get('name')
        phone = request.query_params.get('phone')
        queryset = self.queryset
        if name:
            queryset = queryset.filter(name__icontains=name)
        if phone:
            queryset = queryset.filter(phone__icontains=phone)

        serializer = LeadFilterSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
