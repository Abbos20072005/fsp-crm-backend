from accounting.models import Check, OutcomeType, Outcome, ExpenditureStaff
from rest_framework import serializers


class CheckRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ['amount', 'file', 'student']


class CheckRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ['amount', 'file', 'student']
        extra_kwargs = {
            'file': {'required': False},
            'student': {'required': False},
            'amount': {'required': False},
        }


class OutcomeTypeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeType
        fields = ['name', 'limit']


class OutcomeTypeRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeType
        fields = ['name', 'limit']
        extra_kwargs = {
            'name': {'required': False},
            'limit': {'required': False}
        }


class OutcomeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = ['type', 'amount']


class OutcomeRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = ['type', 'amount']
        extra_kwargs = {
            'type': {'required': False},
            'amount': {'required': False}
        }


class ExpenditureStaffRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenditureStaff
        fields = ['user', 'name', 'description', 'amount']


class ExpenditureStaffRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenditureStaff
        fields = ['user', 'name', 'description', 'amount']
        extra_kwargs = {
            'user': {'required': False},
            'name': {'required': False},
            'description': {'required': False},
            'amount': {'required': False},
        }
