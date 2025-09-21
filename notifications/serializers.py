from rest_framework import serializers
from .models import Notification, EmailTemplate
from accounts.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'notification_type', 'is_read', 
                  'related_object_id', 'created_at', 'read_at']
        read_only_fields = ['user', 'created_at', 'read_at']

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ['id', 'name', 'subject', 'body', 'created_at', 'updated_at']