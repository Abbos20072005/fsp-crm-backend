from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import AdminSerializer,HRSerializer,SuperAdminSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import Admin,SuperAdmin,HR
from drf_yasg import openapi


class AdminPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
class HRViewSet(viewsets.ModelViewSet):

    @swagger_auto_schema(
        operation_description="Create a new admin",
        operation_summary="Add an admin",
        request_body=AdminSerializer,
        responses={
            201: openapi.Response(
                description='Administrator Added Successfully',
            ),
            400: openapi.Response(
                description='Invalid data',
            )
        },
    )
    def create_admin(self, request):
        admin_serializer = AdminSerializer(data=request.data)
        if admin_serializer.is_valid():
            admin_serializer.save()
            return Response(data={"message": "Administrator Added Successfully", "status": status.HTTP_201_CREATED})
        return Response(data={"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete the admin",
        operation_summary="Delete admin",
        responses={
            204: openapi.Response(
                description='Admin deleted successfully',
            ),
            404: openapi.Response(
                description='Admin not found',
            ),
        },
    )
    def delete_admin(self, request, staff_id):
        admin_exists = Admin.objects.filter(pk=staff_id)
        if not admin_exists.exists():
            return Response('Admin not found', status=status.HTTP_404_NOT_FOUND)
        adminstrator = admin_exists.first()
        adminstrator.delete()
        return Response(data={"message": 'Admin deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="List all adminstrators",
        operation_summary="Get all adminstrators",
        responses={
            200: openapi.Response(
                description='List of all adminstrators',
            )
        },
    )


    def retrieve_restaurant(self, request, staff_id):
        exists = Admin.objects.filter(pk=staff_id)
        if not exists.exists():
            return Response(data={'error': 'Adminstrator not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AdminSerializer(exists.first())
        return Response(serializer.data, status=status.HTTP_200_OK)

# Create your views here.
