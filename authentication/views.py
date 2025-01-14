from django.contrib.auth import update_session_auth_hash
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from authentication.models import User, BlacklistedAccessToken
from core.custom_pagination import CustomPagination
from exceptions.error_codes import ErrorCodes
from exceptions.exception import CustomApiException
from .serializers import UserSerializer, UserRegisterSerializer, ChangePasswordSerializer, \
    ChangeUserPasswordSerializer, ChangeUserDetailsSerializer, LogoutSerializer, UserFilterSerializer, \
    SelfChangeUserDetailsSerializer
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
        serializer = UserRegisterSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        user = User.objects.filter(username=data['username'], is_deleted=False).first()
        if not user:
            raise CustomApiException(error_code=ErrorCodes.USER_DOES_NOT_EXIST.value)
        if not check_password(data['password'], user.password):
            raise CustomApiException(ErrorCodes.INVALID_INPUT.value, message='Incorrect password')
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({'access_token': access_token, 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='Access_token')
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
        if not serializer.is_valid():
            return Response(data={'error': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        refresh_token = serializer.validated_data['refresh_token']
        access_token = serializer.validated_data['access_token']
        token1 = RefreshToken(refresh_token)
        token2 = AccessToken(access_token)
        token1.blacklist()
        obj = BlacklistedAccessToken.objects.create(token=token2)
        obj.save()
        return Response(data={'message': 'Token has been added to blacklist', 'ok': True},
                        status=status.HTTP_205_RESET_CONTENT)

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
            raise CustomApiException(ErrorCodes.INVALID_INPUT.value, message='Old password is incorrect')
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
            raise CustomApiException(error_code=ErrorCodes.USER_DOES_NOT_EXIST.value)
        serializer = ChangeUserDetailsSerializer(user, data=request.data, partial=True,
                                                 context={'request': request, 'user_id': user_id})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data={'message': 'User details successfully updated', 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ChangeUserPasswordSerializer,
        responses={
            200: 'Password successfully changed',
            400: 'Invalid data',
            404: 'User not found'
        },
        operation_summary="Change user password by HR and SuperAdmin",
        operation_description="This endpoint allows SuperAdmin or HR to change a user's password."
    )
    @is_super_admin_or_hr
    def change_user_password(self, request, user_id):
        user = User.objects.filter(pk=user_id, is_deleted=False).first()
        if not user:
            raise CustomApiException(error_code=ErrorCodes.USER_DOES_NOT_EXIST.value)
        serializer = ChangeUserPasswordSerializer(data=request.data, context={'request': request, 'user_id': user_id})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        new_password = serializer.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response(data={'message': 'Password successfully changed', 'ok': True}, status=status.HTTP_200_OK)

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
            raise CustomApiException(error_code=ErrorCodes.USER_DOES_NOT_EXIST.value)
        if request.user.role == 3 and user.role == 4:
            raise CustomApiException(error_code=ErrorCodes.USER_DOES_NOT_EXIST.value,
                                     message='You dont have permission to perform this action')
        user.is_deleted = True
        user.save()
        return Response(data={'message': 'User soft deleted successfully', 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description='Page number', type=openapi.TYPE_INTEGER),
            openapi.Parameter('size', openapi.IN_QUERY, description='Size', type=openapi.TYPE_INTEGER),
        ],
        operation_summary='User Filter',
        operation_description='User Filter',
        request_body=UserFilterSerializer,
        responses={200: UserSerializer()},
    )
    @is_super_admin
    def filter_users(self, request):
        serializer = UserFilterSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        page = serializer.validated_data['page']
        size = serializer.validated_data['size']
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
            openapi.Parameter('page', openapi.IN_QUERY, description='Page number', type=openapi.TYPE_INTEGER),
            openapi.Parameter('size', openapi.IN_QUERY, description='Size', type=openapi.TYPE_INTEGER),
        ],
        operation_summary='Search Users',
        operation_description='Search users by username.',
        responses={200: UserSerializer(many=True)},
    )
    def search_user(self, request):
        page = request.query_params.get('page', 1)
        size = request.query_params.get('size', 10)
        query = request.query_params.get('query', "+")
        users = User.objects.filter(is_deleted=False, username__icontains=query).exclude(role=4)
        paginator = CustomPagination()
        paginator.page = page
        paginator.page_size = size
        paginated_users = paginator.paginate_queryset(users, request)

        return paginator.get_paginated_response(
            data={'result': UserSerializer(paginated_users, many=True).data, 'ok': True}
        )


class UserDetailView(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=SelfChangeUserDetailsSerializer,
        responses={
            200: SelfChangeUserDetailsSerializer,
            400: 'Invalid data'
        },
        operation_summary="Update user details",
        operation_description="This endpoint allows a user to update their details."
    )
    @is_employee
    def update(self, request):
        user = request.user
        serializer = SelfChangeUserDetailsSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'message': 'User details successfully updated', 'ok': True},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
