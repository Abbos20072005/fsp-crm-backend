from django.contrib.auth import update_session_auth_hash
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User
from core.custom_pagination import CustomPagination
from .serializers import UserSerializer, UserRegisterSerializer, ChangePasswordSerializer, \
    ChangeUserPasswordSerializer, ChangeUserDetailsSerializer, LogoutSerializer, UserFilterSerializer
from drf_yasg import openapi
from core.BasePermissions import is_super_admin_or_hr, is_employee, is_super_admin


class UserViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        responses={200: UserSerializer()},
        operation_summary="Get user details",
        operation_description="Get user details",
    )
    @is_employee
    def auth_me(self, request):
        user = User.objects.filter(pk=request.user.id).first()
        return Response(data={'result': UserSerializer(user).data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={201: UserRegisterSerializer(), 400: 'Bad Request'},
        operation_summary="Register a new user",
        operation_description="This endpoint allows SuperAdmin or HR to register a new user."
    )
    @is_super_admin_or_hr
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            }
        ),
        responses={
            200: openapi.Response('Login successful', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
            400: 'Incorrect password',
            404: 'User not found'
        },
        operation_summary="User login",
        operation_description="This endpoint allows a user to log in."
    )
    def login(self, request):
        data = request.data
        user = User.objects.filter(username=data['username']).first()
        if not user:
            return Response({'message': 'User with that username not found', 'ok': False},
                            status=status.HTTP_404_NOT_FOUND)
        if check_password(data['password'], user.password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token, 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
        return Response({'error': 'Incorrect password', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token')
            }
        ),
        responses={
            205: 'Token has been added to blacklist',
            400: 'Refresh token not provided'
        },
        operation_summary="User logout",
        operation_description="This endpoint allows a user to log out."
    )
    @is_employee
    def logout(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Token has been added to blacklist', 'ok': True},
                            status=status.HTTP_205_RESET_CONTENT)
        return Response({'error': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        responses={
            200: 'Password successfully changed',
            400: 'Invalid data or old password is incorrect'
        },
        operation_summary="Change user password",
        operation_description="This endpoint allows a user to change their password."
    )
    @is_employee
    def change_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        old_password = serializer.data.get('old_password')
        new_password = serializer.data.get('new_password')
        if not user.check_password(old_password):
            return Response(
                data={'error': 'Old password is incorrect!', 'ok': False},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Password Hashing
        return Response(
            data={'message': 'password successfully changed', 'ok': True},
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_PATH, description="User ID", type=openapi.TYPE_INTEGER),
        ],
        request_body=ChangeUserDetailsSerializer,
        responses={
            200: ChangeUserDetailsSerializer,
            400: 'Invalid data',
            404: 'User not found'
        },
        operation_summary="Update user information",
        operation_description="This endpoint allows SuperAdmin or HR to update user information."
    )
    @is_super_admin_or_hr
    def update_user(self, request, user_id):
        user = User.objects.filter(pk=user_id, is_deleted=False).first()
        if not user:
            return Response({'message': 'User not found', 'ok': False}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChangeUserDetailsSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'message': 'User details successfully updated', 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ChangeUserPasswordSerializer,
        responses={
            200: 'Password successfully changed',
            400: 'Invalid data',
            404: 'User not found'
        },
        operation_summary="Change user password (Admin)",
        operation_description="This endpoint allows SuperAdmin or HR to change a user's password."
    )
    @is_super_admin_or_hr
    def change_user_password(self, request, user_id):
        user = User.objects.filter(pk=user_id, is_deleted=False).first()
        if not user:
            return Response({'message': 'User not found', 'ok': False}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChangeUserPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        new_password = serializer.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password successfully changed', 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_PATH, description="User ID", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: 'User soft deleted successfully',
            404: 'User not found'
        },
        operation_summary="Soft delete user",
        operation_description="Soft delete user"
    )
    @is_super_admin_or_hr
    def soft_delete(self, request, user_id):
        user = User.objects.filter(pk=user_id, is_deleted=False).first()
        if not user:
            return Response(data={'message': 'User not found', 'ok': False}, status=status.HTTP_404_NOT_FOUND)
        user.is_deleted = True
        user.save(update_fields=['is_deleted'])
        return Response(data={'message': 'User soft deleted successfully', 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description='Page number', type=openapi.TYPE_INTEGER),
            openapi.Parameter('size', openapi.IN_QUERY, description='Size', type=openapi.TYPE_INTEGER),
        ],
        operation_summary='User Filter',
        operation_description='User Filter',
        request_body=UserFilterSerializer(),
        responses={200: UserSerializer()},
    )

    #@is_super_admin
    def filter_users(self, request):
        page = int(request.query_params.get('page', 1))
        size = int(request.query_params.get('size', 10))

        serializer = UserFilterSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        role = serializer.validated_data.get('role')
        kpi = serializer.validated_data.get('kpi')
        fixed_salary = serializer.validated_data.get('fixed_salary')
        created_at = serializer.validated_data.get('created_at')

        result = {}
        if role is not None:
            result['role'] = role
        if kpi is not None:
            result['kpi__gte'] = kpi
        if fixed_salary is not None:
            result['fixed_salary__gte'] = fixed_salary
        if created_at is not None:
            result['created_at__gte'] = created_at

        users = User.objects.filter(**result)

        paginator = CustomPagination()
        paginator.page = page
        paginator.page_size = size
        paginated_users = paginator.paginate_queryset(users, request)

        return paginator.get_paginated_response(
            data={'result': UserSerializer(paginated_users, many=True).data, 'ok': True}
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, description='Search query for username',
                              type=openapi.TYPE_STRING),
        ],
        operation_summary='Search Users',
        operation_description='Search users by username.',
        responses={200: UserSerializer(many=True)},
    )
    def search_user(self, request):
        query = request.GET.get('query', "")
        users = User.objects.filter(is_deleted=False, username__icontains=query).exclude(role=4)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
