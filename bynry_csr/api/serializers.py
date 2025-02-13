from rest_framework import serializers
from .models import ServiceRequest, ServiceRequestAttachment, User

class ServiceRequestAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = ServiceRequestAttachment
        fields = ['id', 'file', 'file_url', 'uploaded_at']

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None

class ServiceRequestSerializer(serializers.ModelSerializer):
    attachments = ServiceRequestAttachmentSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = ServiceRequest
        fields = ['id', 'user', 'service_type', 'details', 'status', 'submission_date', 'resolution_date', 'status_history', 'attachments']

class UserSerializer(serializers.ModelSerializer):
    service_requests = ServiceRequestSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'phone', 'email', 'address', 'service_requests'] 