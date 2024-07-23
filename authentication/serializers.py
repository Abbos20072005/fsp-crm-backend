from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from .models import User
from .utils import is_valid_token


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


class ChangeUserPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate_refresh_token(self, value):
        if not is_valid_token(value):
            raise serializers.ValidationError('Token is invalid or expired')
        blacklisted_token = BlacklistedToken.objects.filter(token__token=value).exists()
        if blacklisted_token:
            raise serializers.ValidationError('Token is already in blacklist')
        return value


class UserFilterSerializer(serializers.Serializer):
    role = serializers.IntegerField(required=False)
    kpi = serializers.DecimalField(required=False, max_digits=15, decimal_places=2)
    fixed_salary = serializers.DecimalField(required=False, max_digits=15, decimal_places=2)
    created_at = serializers.DateTimeField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=False)

    def validate(self, data):
        role = data.get('role', None)
        if role is not None and role not in [1, 2, 3]:
            raise ValidationError({"role": "Role must be one of the following values: 1, 2, 3."})
        return data
