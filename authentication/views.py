from django.contrib.auth import update_session_auth_hash
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User
from .serializers import UserRegisterSerializer, ChangePasswordSerializer, UserUpdateSerializer, \
    ChangeUserPasswordSerializer
from drf_yasg import openapi
from core.BasePermissions import is_super_admin_or_hr, is_employee


class UserViewSet(viewsets.ViewSet):
    @is_super_admin_or_hr
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    @is_employee
    def logout(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token not provided', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Token has been added to blacklist', 'ok': True},
                        status=status.HTTP_205_RESET_CONTENT)

    @is_employee
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

    def update(self, request, pk):
        user = User.objects.get(pk=pk)
        if user:
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'User not found', 'ok': False}, status=status.HTTP_404_NOT_FOUND)

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
