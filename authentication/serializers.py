from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


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

    def validate(self, attrs):
        role = self.context['request'].user.role
        if role == 'HR' and 'role' in attrs:
            if attrs['role'] != 'Admin':
                raise serializers.ValidationError("HR can only assign 'Admin' role.")
        return attrs


class ChangeUserPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
