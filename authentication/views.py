from django.contrib.auth import update_session_auth_hash
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User
from .serializers import UserRegisterSerializer, ChangePasswordSerializer, UserUpdateSerializer, \
    ChangeUserPasswordSerializer
from .permissions import IsSuperAdminOrHR, IsEmployee
from drf_yasg import openapi



class UserViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={201: UserRegisterSerializer, 400: 'Bad Request'},
        operation_summary="Register a new user",
        operation_description="This endpoint allows SuperAdmin or HR to register a new user.")

    @action(detail=True, permission_classes=[IsSuperAdminOrHR])
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, description="Username of the user", type=openapi.TYPE_STRING,
                              required=True),
            openapi.Parameter('password', openapi.IN_FORM, description="Password of the user", type=openapi.TYPE_STRING,
                              required=True)
        ],
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token")
                    }
                )
            ),
            404: openapi.Response(description="User not found"),
            400: openapi.Response(description="Incorrect password")
        },
        operation_summary="User login",
        operation_description="This endpoint allows a user to log in and get access and refresh tokens.")

    @action(detail=True, permission_classes=[IsEmployee])
    def login(self, request):
        data = request.data
        user = User.objects.filter(username=data['username']).first()
        if not user:
            return Response({'message': 'User not found', 'ok': False}, status=status.HTTP_404_NOT_FOUND)
        if check_password(data['password'], user.password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token, 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
        return Response({'error': 'Incorrect password', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token",
                                                example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
            },
            required=['refresh_token']
        ),
        responses={
            205: openapi.Response(description="Token has been added to blacklist"),
            400: openapi.Response(description="Refresh token not provided")
        },
        operation_summary="Logout a user",
        operation_description="This endpoint allows a user to log out by blacklisting the refresh token."
    )

    @action(detail=True, permission_classes=[IsEmployee])
    def logout(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token not provided', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Token has been added to blacklist', 'ok': True},
                        status=status.HTTP_205_RESET_CONTENT)

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        responses={
            200: openapi.Response(description="Password successfully changed"),
            400: openapi.Response(description="Old password is incorrect!")
        },
        operation_summary="Change the password of the logged-in user",
        operation_description="This endpoint allows a user to change their own password."
    )
    @action(detail=True, permission_classes=[IsEmployee])
    def change_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response(
                    data={'error': 'Old password is incorrect!', 'ok': False},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Set password and save
            user.set_password(serializer.data.get('new_password'))
            user.save()
            update_session_auth_hash(request, user)  # Password Hashing

            return Response(
                data={'message': 'password successfully changed', 'ok': True},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={
            200: openapi.Response(description="User updated successfully", schema=UserUpdateSerializer),
            404: openapi.Response(description="User not found"),
            400: openapi.Response(description="Bad Request")
        },
        operation_summary="Update a user's role, username, or salary",
        operation_description="This endpoint allows SuperAdmin or HR to update a user's role, username, or salary."
    )
    @action(detail=True, permission_classes=[IsSuperAdminOrHR])
    def update(self, request, pk):
        user = User.objects.get(pk=pk)
        if user:
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'User not found', 'ok': False}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=ChangeUserPasswordSerializer,
        responses={
            200: openapi.Response(description="Password successfully changed"),
            404: openapi.Response(description="User not found"),
            400: openapi.Response(description="Bad Request")
        },
        operation_summary="Change another user's password",
        operation_description="This endpoint allows SuperAdmin or HR to change another user's password."
    )
    @action(detail=True, permission_classes=[IsSuperAdminOrHR])
    def change_user_password(self, request, pk):
        user = User.objects.get(pk=pk)
        if user:
            serializer = ChangeUserPasswordSerializer(data=request.data)
            if serializer.is_valid():
                new_password = serializer.data.get('new_password')
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password successfully changed', 'ok': True}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'User not found', 'ok': False}, status=status.HTTP_404_NOT_FOUND)

