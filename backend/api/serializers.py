"""
Serializers for Chemical Equipment Analysis API.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Equipment, Upload


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User registration."""
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class EquipmentSerializer(serializers.ModelSerializer):
    """Serializer for Equipment model."""
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'type', 'flowrate', 'pressure', 'temperature']


class UploadSerializer(serializers.ModelSerializer):
    """Serializer for Upload model."""
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Upload
        fields = ['id', 'filename', 'uploaded_at', 'record_count', 'equipment_count']
    
    def get_equipment_count(self, obj):
        return obj.equipment.count()


class UploadDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Upload including equipment list."""
    equipment = EquipmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Upload
        fields = ['id', 'filename', 'uploaded_at', 'record_count', 'equipment']


class SummarySerializer(serializers.Serializer):
    """Serializer for summary statistics."""
    total_count = serializers.IntegerField()
    avg_flowrate = serializers.FloatField()
    avg_pressure = serializers.FloatField()
    avg_temperature = serializers.FloatField()
    min_flowrate = serializers.FloatField()
    max_flowrate = serializers.FloatField()
    min_pressure = serializers.FloatField()
    max_pressure = serializers.FloatField()
    min_temperature = serializers.FloatField()
    max_temperature = serializers.FloatField()
    type_distribution = serializers.DictField()
