"""
URL routing for Chemical Equipment Analysis API.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    
    # Data endpoints
    path('upload/', views.CSVUploadView.as_view(), name='upload'),
    path('data/', views.EquipmentListView.as_view(), name='equipment-list'),
    path('summary/', views.SummaryView.as_view(), name='summary'),
    path('history/', views.UploadHistoryView.as_view(), name='upload-history'),
    path('history/<int:pk>/', views.UploadDetailView.as_view(), name='upload-detail'),
    path('report/', views.PDFReportView.as_view(), name='pdf-report'),
]
