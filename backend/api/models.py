"""
Models for Chemical Equipment Analysis API.
"""
from django.db import models
from django.contrib.auth.models import User


class Upload(models.Model):
    """Represents a CSV file upload session."""
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    record_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.filename} ({self.record_count} records)"
    
    @classmethod
    def cleanup_old_uploads(cls, user, keep_count=5):
        """Keep only the last N uploads for a user, delete older ones."""
        uploads = cls.objects.filter(user=user).order_by('-uploaded_at')
        uploads_to_delete = uploads[keep_count:]
        for upload in uploads_to_delete:
            upload.delete()


class Equipment(models.Model):
    """Represents a piece of chemical equipment."""
    EQUIPMENT_TYPES = [
        ('Pump', 'Pump'),
        ('Compressor', 'Compressor'),
        ('Valve', 'Valve'),
        ('HeatExchanger', 'Heat Exchanger'),
        ('Reactor', 'Reactor'),
        ('Condenser', 'Condenser'),
        ('Other', 'Other'),
    ]
    
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=EQUIPMENT_TYPES)
    flowrate = models.FloatField(help_text="Flowrate in units")
    pressure = models.FloatField(help_text="Pressure in bar")
    temperature = models.FloatField(help_text="Temperature in °C")
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, related_name='equipment')
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Equipment"
    
    def __str__(self):
        return f"{self.name} ({self.type})"
