from rest_framework import serializers

from authentication.models import User
from .models import Lead, Comment


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'name', 'phone', 'address', 'status', 'created_at']


class LeadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['admin', 'name', 'phone', 'address']


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
