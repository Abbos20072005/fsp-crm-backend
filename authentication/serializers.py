from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from .models import User, BlacklistedAccessToken
from .utils import is_valid_tokens


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user

    def validate(self, data):
        request = self.context.get('request')
        role = data.get('role', None)
        if request.user.role == 3 and role == 4:
            raise ValidationError({"message": "Allowed roles for HR to create: 1, 2, 3."})
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'kpi', 'fixed_salary', 'created_at']


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangeUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'role', 'fixed_salary']
        extra_kwargs = {
            'username': {'required': False},
            'role': {'required': False},
            'fixed_salary': {'required': False},
        }

    def validate(self, data):
        user = User.objects.get(user_id=self.context.get('user_id'))
        request = self.context.get('request')
        if request.user.role == 3 and user.role == 4:
            raise ValidationError({'You are not allowed to change details of this user'})
        role = data.get('role', None)
        if request.user.role == 3 and role == 4:
            raise ValidationError({'You are not allowed promote to super admin'})
        return data


class ChangeUserPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.get(user_id=self.context.get('user_id'))
        request = self.context.get('request')
        if request.user.role == 3 and user.role == 4:
            raise ValidationError({'You are not allowed to change details of this user'})
        return data


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
    access_token = serializers.CharField(required=True)

    def validate(self, data):
        refresh_token = data.get('refresh_token')
        access_token = data.get('access_token')
        if not is_valid_tokens(refresh_token, access_token):
            raise serializers.ValidationError('Access token or Refresh token is invalid or expired')
        refresh_blacklisted = BlacklistedToken.objects.filter(token__token=refresh_token).exists()
        access_blacklisted = BlacklistedAccessToken.objects.filter(token=access_token).exists()

        if refresh_blacklisted or access_blacklisted:
            raise serializers.ValidationError('Tokens are already in blacklist')
        return data


class UserFilterSerializer(serializers.Serializer):
    role = serializers.IntegerField(required=False)
    kpi = serializers.DecimalField(required=False, max_digits=15, decimal_places=2)
    fixed_salary = serializers.DecimalField(required=False, max_digits=15, decimal_places=2)

    def validate(self, data):
        role = data.get('role', None)
        if role is not None and role not in [1, 2, 3]:
            raise ValidationError({"role": "Role must be one of the following values: 1, 2, 3."})
        return data
