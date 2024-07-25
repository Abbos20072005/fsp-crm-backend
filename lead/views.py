from datetime import date, datetime

from django.core.paginator import Paginator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from authentication.models import User
from .models import Lead
from .permissions import check_role
from .serializer import LeadCreateSerializer, LeadUpdateSerializer, LeadSerializer, CommentSerializer, \
    LeadStatusSerializer, MyLeadSerializer

from django.db.models import Q, Sum
from .serializer import LeadCreateSerializer, LeadUpdateSerializer, LeadSerializer, LeadFilterSerializer
from accounting.models import Check, ExpenditureStaff


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


class MyLeadViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Admin Dashboard",
        operation_summary="Admin Dashboard",
        manual_parameters=[
            openapi.Parameter('start_date', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY),
            openapi.Parameter('end_date', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY),
            openapi.Parameter('lead_status', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY),
        ],
        responses={200: MyLeadSerializer()},
        tags=['admin_dashboard']
    )
    def my_leads(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            lead_status = request.GET.get('lead_status')
            if start_date or end_date:
                filter_query = Q(admin=user)

                if start_date:
                    filter_query &= Q(created_at__gte=start_date)

                if end_date:
                    filter_query &= Q(created_at__lte=end_date)

                if lead_status:
                    filter_query &= Q(status=lead_status)

                my_leads = Lead.objects.filter(filter_query)

            else:
                my_leads = Lead.objects.filter(admin=user)

            total = len(my_leads)
            serializer = MyLeadSerializer(my_leads, many=True, context={"total": total})
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({"error": "user is not authenticated"}, status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        operation_description="Admin Dashboard",
        operation_summary="Admin Dashboard",
        manual_parameters=[
            openapi.Parameter('salary_month', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY),
            openapi.Parameter('salary_year', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY),
        ],
        responses={200: "Information returns"},
        tags=['admin_dashboard']
    )
    def my_salary(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            salary_month = request.GET.get('salary_month')
            salary_year = request.GET.get('salary_year')
            if salary_year or salary_month:
                data = self.salary_calculation(user.id, year=salary_year, month=salary_month)
            else:
                date = self.salary_calculation(user.id, year=datetime.year, month=datetime.month)
            return Response(data, status.HTTP_200_OK)
        return Response({"error": "user is not authenticated"}, status.HTTP_401_UNAUTHORIZED)

    def salary_calculation(self, pk, year=None, month=None):
        admin = User.objects.filter(id=pk, is_deleted=False).first()
        filter_query = Q()
        if year:
            filter_query &= Q(created_at__year=year)
        if month:
            filter_query &= Q(created_at__month=month)
        kpi_from_check = Check.objects.filter(uploaded_by=pk).filter(filter_query).count()
        expenditure = ExpenditureStaff.objects.filter(user_id=pk, is_deleted=False).order_by('-created_at')
        minus = expenditure.values('amount').distinct().aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        data = {
            'student_quantity': kpi_from_check,
            'kpi_amount': kpi_from_check * admin.kpi,
            'fixed_salary': admin.fixed_salary,
            'fine': minus,
            'salary_this_month': kpi_from_check * admin.kpi + admin.fixed_salary - minus
        }
        return data
