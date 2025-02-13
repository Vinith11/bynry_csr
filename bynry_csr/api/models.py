from django.db import models
import os
from django.db.models import JSONField

# Create your models here.

def get_upload_path(instance, filename):
    # Create path in format: attachments/service_request_id/filename
    return os.path.join('attachments', str(instance.service_request.id), filename)

class ServiceRequestAttachment(models.Model):
    service_request = models.ForeignKey('ServiceRequest', related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.service_request.service_type} - {self.file.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class User(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name

class ServiceRequest(models.Model):
    SERVICE_TYPES = [
        ('installation', 'Installation'),
        ('repair', 'Repair'),
        ('maintenance', 'Maintenance'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    user = models.ForeignKey(User, related_name='service_requests', on_delete=models.CASCADE, null=True, blank=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    details = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submission_date = models.DateTimeField(auto_now_add=True)
    resolution_date = models.DateTimeField(null=True, blank=True)
    status_history = JSONField(default=dict)

    def __str__(self):
        return f"{self.service_type} - {self.status}"

    def save(self, *args, **kwargs):
        is_new = not self.pk
        if is_new:
            # For new records, set the initial status history before saving
            self.status_history = {}
        super().save(*args, **kwargs)
        if is_new:
            # Update the status history with the submission date after the first save
            self.status_history['pending'] = self.submission_date.isoformat()
            super().save(update_fields=['status_history'])
