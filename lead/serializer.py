from rest_framework import serializers

from authentication.models import User
from .models import Lead, Comment
from .models import Lead, Comment, Student, StudentDocuments, DocumentType


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'name', 'phone', 'address', 'status', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['comments'] = CommentListSerializer(Comment.objects.filter(lead_id=instance.id), many=True).data
        return data


class LeadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'admin', 'name', 'phone', 'address']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']

    def create(self, validated_data):
        author_id = self.context['request'].user.id
        lead_id = self.context['lead_id']
        comment = Comment.objects.create(author_id=author_id, lead_id=lead_id, comment=validated_data['comment'])
        return comment


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']


class LeadUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ["admin", "name", "phone", "status", "address"]


# TODO check the students

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'full_name', 'phone', 'passport_number', 'personal_number', 'lead', 'address', 'admin']

    def to_representation(self, instance):
        instance = super(StudentSerializer, self).to_representation(instance)
        return instance


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'name']


class StudentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDocuments
        fields = ['id', 'document', 'name', 'student']


class MakeStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'full_name', 'phone', 'lead']


class BulkUpdateAdminSerializer(serializers.Serializer):
    lead_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        error_messages={
            'empty': 'Lead IDs cannot be empty.',
            'invalid': 'Lead IDs must be a list of integers.',
        }
    )
    new_admin_id = serializers.IntegerField(
        error_messages={
            'required': 'New admin ID is required.',
            'invalid': 'New admin ID must be an integer.'
        }
    )

    def validate_lead_ids(self, value):
        """ Ensure all lead_ids exist """
        if not Lead.objects.filter(id__in=value).count() == len(value):
            raise serializers.ValidationError('Some lead IDs are invalid or not found.')
        return value

    def validate_new_admin_id(self, value):
        """ Ensure the new_admin_id exists """
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError('New admin not found.')
        return value


class MyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class MyLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ('id', 'name', 'phone', 'status', 'address', 'admin', 'created_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['comments'] = MyCommentSerializer(Comment.objects.filter(lead=data['id']), many=True).data
        data['total'] = self.context.get('total', None)
        data['interested_leads'] = self.context.get('interested_leads', None)
        data['possible_leads'] = self.context.get('possible_leads', None)
        data['joined_leads'] = self.context.get('joined_leads', None)
        data['canceled_leads'] = self.context.get('canceled_leads', None)
        return data


class LeadStatsSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100)
    interested = serializers.IntegerField(default=0)
    possible = serializers.IntegerField(default=0)
    joined = serializers.IntegerField(default=0)
    cancelled = serializers.IntegerField(default=0)
    total_amount = serializers.FloatField(default=0)


class LeadCountSerializer(serializers.Serializer):
    total = serializers.IntegerField(default=0)
    interested = serializers.IntegerField(default=0)
    possible = serializers.IntegerField(default=0)
    joined = serializers.IntegerField(default=0)
    cancelled = serializers.IntegerField(default=0)


class HRStatisticsSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

class AdditionalStatisticsSerializer(serializers.Serializer):
    filter = serializers.ChoiceField(
        choices=['status', 'source', 'students', 'daily', 'weekly', 'monthly', 'yearly'],
        required=False
    )
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

