from rest_framework import serializers
from .models import Lead, Comment, Student, StudentDocuments


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'name', 'phone', 'address', 'status', 'created_at']


class LeadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['status', ]


class LeadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['admin', 'name', 'phone', 'address']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment']


class LeadUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ["admin", "name", "phone", "status", "address"]


# TODO check the students

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'full_name', 'phone', 'passport_number', 'personal_number']

    def to_representation(self, instance):
        instance = super(StudentSerializer, self).to_representation(instance)
        return instance


class StudentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDocuments
        fields = ['id', 'document', 'name']
