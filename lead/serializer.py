from rest_framework import serializers
from .models import Lead, Comment


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


class LeadFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'


class MyLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ('id', 'name', 'phone', 'status', 'address', 'admin', 'created_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['comments'] = CommentSerializer(Comment.objects.filter(lead=data['id']), many=True).data
        data['total'] = self.context.get('total', None)
        return data
