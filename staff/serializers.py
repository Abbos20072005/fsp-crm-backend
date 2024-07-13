from .models import HR,Admin,SuperAdmin
from rest_framework import serializers

class HRSerializer(serializers.ModelSerializer):
    class Meta:
        model = HR
        fields = ['phone','email','date_of_birth','hire_date']

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['phone','email','date_of_birth','hire_date']

class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = ['phone','email','date_of_birth','hire_date']