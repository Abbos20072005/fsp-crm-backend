from datetime import date, datetime, timedelta

from django.core.paginator import Paginator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from authentication.models import User
from .models import Lead, Comment, STATUS_CHOICES

from authentication.models import User
from .models import Lead
from .permissions import check_role
from .serializer import LeadCreateSerializer, LeadUpdateSerializer, LeadSerializer, \
    CommentCreateSerializer, CommentListSerializer, BulkUpdateAdminSerializer, LeadStatsSerializer, LeadCountSerializer
from .serializer import LeadCreateSerializer, LeadUpdateSerializer, LeadSerializer, MyLeadSerializer

from django.db.models import Q, Sum, Count, Case, When, IntegerField
from .serializer import LeadCreateSerializer, LeadUpdateSerializer, LeadSerializer
from accounting.models import Check, ExpenditureStaff, Salary
from core.BasePermissions import is_super_admin_or_hr, is_admin_or_super_admin, is_super_admin


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


class LeadStatsViewSet(ViewSet):
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
    @is_admin_or_super_admin
    def my_salary(self, request, *args, **kwargs):
        user = request.user
        salary_month = request.GET.get('salary_month')
        salary_year = request.GET.get('salary_year')

        if salary_year or salary_month:
            data = self.salary_calculation(user.id, year=salary_year, month=salary_month)
        else:
            data = self.salary_calculation(user.id, year=datetime.year, month=datetime.month)
        return Response(data, status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Admin Dashboard",
        operation_summary="Admin Dashboard",
        manual_parameters=[
            openapi.Parameter('lead_year', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY),
            openapi.Parameter('lead_month', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY),
        ],
        responses={200: MyLeadSerializer()},
        tags=['admin_dashboard']
    )
    @is_admin_or_super_admin
    def my_leads(self, request, *args, **kwargs):
        user = request.user
        lead_year = request.GET.get('lead_year')
        lead_month = request.GET.get('lead_month')
        if lead_year or lead_month:
            filter_query = Q()
            if lead_year:
                filter_query &= Q(created_at__year=lead_year)
            if lead_month:
                filter_query &= Q(created_at__month=lead_month)
            leads = Lead.objects.filter(admin=user).filter(filter_query)
        else:
            leads = Lead.objects.filter(admin=user)
        leads_stats = leads.aggregate(
            total=Count('id'),
            interested_leads=Count(Case(When(status=1, then=1), output_field=IntegerField())),
            possible_leads=Count(Case(When(status=2, then=1), output_field=IntegerField())),
            joined_leads=Count(Case(When(status=3, then=1), output_field=IntegerField())),
            canceled_leads=Count(Case(When(status=4, then=1), output_field=IntegerField()))
        )
        serializer = MyLeadSerializer(leads, context={"total": leads_stats['total'],
                                                      "interested_leads": leads_stats['interested_leads'],
                                                      "possible_leads": leads_stats['possible_leads'],
                                                      "joined_leads": leads_stats['joined_leads'],
                                                      "canceled_leads": leads_stats['canceled_leads']})
        return Response(serializer.data, status.HTTP_200_OK)

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

    @swagger_auto_schema(
        operation_description='Admin Dashboard',
        operation_summary='Admin Dashboard',
        manual_parameters=[
            openapi.Parameter('start_date', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY),
            openapi.Parameter('to_date', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY),
        ],
        responses={200: LeadStatsSerializer()},
        tags=['admin_dashboard']
    )
    @is_super_admin
    def sum_leads(self, request, *args, **kwargs):
        data = request.query_params
        start_date = data.get('start_date', datetime.now() - timedelta(days=15))
        to_date = data.get('to_date', str(datetime.now().date()))
        leads = Lead.objects.filter(updated_at__lte=to_date + ' 23:59:59', updated_at__gte=start_date, is_deleted=False,
                                    admin__isnull=False).values('status', 'admin', 'admin__first_name',
                                                                'admin__last_name')
        leads_ = []
        for lead in leads:
            full_name = lead['admin__first_name'] + ' ' + lead['admin__last_name']
            for lead_ in leads_:
                if full_name == lead_['full_name']:
                    lead_[STATUS_CHOICES[lead['status'] - 1][1].lower()] += 1
                    break
            else:
                d = {'full_name': full_name, 'interested': 0, 'possible': 0, 'joined': 0, 'cancelled': 0}
                d[STATUS_CHOICES[lead['status'] - 1][1].lower()] += 1
                leads_.append(d)

        for i in range(len(leads_)):
            check_count = Check.objects.filter(updated_at__lte=to_date + ' 23:59:59',
                                               updated_at__gte=start_date,
                                               uploaded_by_id=leads[i]['admin'],
                                               is_deleted=False, is_confirmed=True).values('student').distinct().count()
            kpi = Salary.objects.filter(user_id=leads[i]['admin']).first().kpi_amount
            leads_[i]['total_amount'] = kpi * check_count

        serializer = LeadStatsSerializer(leads_, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Admin Dashboard',
        operation_summary='Admin Dashboard',
        manual_parameters=[
            openapi.Parameter('year', type=openapi.TYPE_STRING, in_=openapi.IN_QUERY),
        ],
        responses={200: LeadCountSerializer()},
        tags=['admin_dashboard']
    )
    @is_super_admin
    def count_leads(self, request, *args, **kwargs):
        year = request.query_params.get('year', datetime.now().year)
        status_ = lambda num: Count("status", filter=Q(status=num))

        leads = Lead.objects.filter(updated_at__year=year).aggregate(interested=status_(1),
                                                                     possible=status_(2),
                                                                     joined=status_(3),
                                                                     cancelled=status_(4),
                                                                     total=Count('id'))
        serializer = LeadCountSerializer(leads)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
