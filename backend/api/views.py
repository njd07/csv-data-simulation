"""
API Views for Chemical Equipment Analysis.
"""
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Equipment, Upload
from .serializers import (
    UserSerializer, EquipmentSerializer, UploadSerializer,
    UploadDetailSerializer, SummarySerializer
)
from .utils import parse_csv, calculate_summary, generate_pdf_report


class RegisterView(generics.CreateAPIView):
    """User registration endpoint."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """User login endpoint."""
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            })
        
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class CSVUploadView(APIView):
    """Handle CSV file uploads."""
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        file = request.FILES.get('file')
        
        if not file:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not file.name.endswith('.csv'):
            return Response(
                {'error': 'File must be a CSV'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse CSV
        equipment_list, error = parse_csv(file)
        
        if error:
            return Response(
                {'error': f'Failed to parse CSV: {error}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not equipment_list:
            return Response(
                {'error': 'CSV file contains no valid data'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create upload record
        upload = Upload.objects.create(
            filename=file.name,
            user=request.user,
            record_count=len(equipment_list)
        )
        
        # Create equipment records
        equipment_objects = [
            Equipment(
                name=eq['name'],
                type=eq['type'],
                flowrate=eq['flowrate'],
                pressure=eq['pressure'],
                temperature=eq['temperature'],
                upload=upload
            )
            for eq in equipment_list
        ]
        Equipment.objects.bulk_create(equipment_objects)
        
        # Cleanup old uploads (keep only last 5)
        Upload.cleanup_old_uploads(request.user, keep_count=5)
        
        return Response({
            'message': 'Upload successful',
            'upload': UploadSerializer(upload).data,
            'equipment_count': len(equipment_list)
        }, status=status.HTTP_201_CREATED)


class EquipmentListView(generics.ListAPIView):
    """List equipment data for current user's latest upload."""
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        upload_id = self.request.query_params.get('upload_id')
        
        if upload_id:
            return Equipment.objects.filter(
                upload_id=upload_id,
                upload__user=self.request.user
            )
        
        # Get latest upload for user
        latest_upload = Upload.objects.filter(user=self.request.user).first()
        if latest_upload:
            return Equipment.objects.filter(upload=latest_upload)
        
        return Equipment.objects.none()


class SummaryView(APIView):
    """Return summary statistics for equipment data."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        upload_id = request.query_params.get('upload_id')
        
        if upload_id:
            queryset = Equipment.objects.filter(
                upload_id=upload_id,
                upload__user=request.user
            )
        else:
            latest_upload = Upload.objects.filter(user=request.user).first()
            if latest_upload:
                queryset = Equipment.objects.filter(upload=latest_upload)
            else:
                queryset = Equipment.objects.none()
        
        summary = calculate_summary(queryset)
        serializer = SummarySerializer(summary)
        return Response(serializer.data)


class UploadHistoryView(generics.ListAPIView):
    """List upload history (last 5 uploads)."""
    serializer_class = UploadSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Upload.objects.filter(user=self.request.user)[:5]


class UploadDetailView(generics.RetrieveAPIView):
    """Get details of a specific upload."""
    serializer_class = UploadDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Upload.objects.filter(user=self.request.user)


class PDFReportView(APIView):
    """Generate and download PDF report."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        upload_id = request.query_params.get('upload_id')
        
        if upload_id:
            queryset = Equipment.objects.filter(
                upload_id=upload_id,
                upload__user=request.user
            )
        else:
            latest_upload = Upload.objects.filter(user=request.user).first()
            if latest_upload:
                queryset = Equipment.objects.filter(upload=latest_upload)
            else:
                return Response(
                    {'error': 'No data available for report'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        if not queryset.exists():
            return Response(
                {'error': 'No equipment data found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        summary = calculate_summary(queryset)
        pdf_buffer = generate_pdf_report(queryset, summary)
        
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="equipment_report.pdf"'
        return response
