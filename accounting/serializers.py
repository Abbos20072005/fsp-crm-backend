from authentication.models import User
from .models import Check, OutcomeType, Outcome, Salary
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'role', 'kpi', 'fixed_salary')


class CheckSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = Check
        fields = ['id', 'uploaded_by', 'amount', 'file', 'student', ]
        extra_kwargs = {
            'file': {'required': False},
            'student': {'required': False}
        }


class OutcomeTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = OutcomeType
        fields = ['id', 'name', 'limit']


class OutcomeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Outcome
        fields = ['id', 'type', 'amount', ]


class OutcomeFilterSerializer(serializers.Serializer):
    type = serializers.IntegerField(required=False)
    time_from = serializers.DateTimeField(required=False)
    time_to = serializers.DateTimeField(required=False)






