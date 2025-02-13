from django.db import models
import os
from django.db.models import JSONField

# Create your models here.

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

    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    details = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submission_date = models.DateTimeField(auto_now_add=True)
    resolution_date = models.DateTimeField(null=True, blank=True)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    status_history = JSONField(default=dict)

    def __str__(self):
        return f"{self.service_type} - {self.status}"

    def save(self, *args, **kwargs):
        is_new = not self.pk
        if is_new:
            # For new records, set the initial status history before saving
            self.status_history = {}
        if self.attachment:
            self.attachment.name = os.path.join('report', self.attachment.name)
        super().save(*args, **kwargs)
        if is_new:
            # Update the status history with the submission date after the first save
            self.status_history['pending'] = self.submission_date.isoformat()
            super().save(update_fields=['status_history'])
