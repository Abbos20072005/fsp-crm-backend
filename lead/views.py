from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Lead
from .permissions import check_role
from .serializer import LeadCreateSerializer, LeadUpdateSerializer, LeadSerializer, CommentSerializer, \
    LeadStatusSerializer, MyLeadSerializer

from django.db.models import Q


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


class MyLeadViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Admin Dashboard",
        operation_summary="Admin Dashboard",
        manual_parameters=[
            openapi.Parameter('start_date', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY),
            openapi.Parameter('end_date', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY),
        ],
        responses={200: MyLeadSerializer()},
        tags=['admin_dashboard']
    )
    def my_leads(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')

            if start_date or end_date:
                filter_query = Q(admin=user)

                if start_date:
                    filter_query &= Q(created_at__gte=start_date)

                if end_date:
                    filter_query &= Q(created_at__lte=end_date)

                my_leads = Lead.objects.filter(filter_query)

            else:
                my_leads = Lead.objects.filter(admin=user)

            total = len(my_leads)
            serializer = MyLeadSerializer(my_leads, many=True, context={"total": total})
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({"error": "user is not authenticated"}, status.HTTP_401_UNAUTHORIZED)
