from django.contrib import admin
from .models import Equipment, Upload


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'record_count', 'uploaded_at']
    list_filter = ['user', 'uploaded_at']
    search_fields = ['filename']
    readonly_fields = ['uploaded_at']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'flowrate', 'pressure', 'temperature', 'upload']
    list_filter = ['type', 'upload']
    search_fields = ['name']
