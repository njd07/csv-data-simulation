"""
Utility functions for CSV parsing and PDF generation.
"""
import io
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from django.db.models import Avg, Min, Max, Count


def parse_csv(file):
    """
    Parse uploaded CSV file and return equipment data as list of dicts.
    
    Args:
        file: File-like object containing CSV data
        
    Returns:
        tuple: (list of equipment dicts, error message or None)
    """
    try:
        df = pd.read_csv(file)
        
        # Validate required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return None, f"Missing columns: {', '.join(missing_columns)}"
        
        # Clean and validate data
        df = df.dropna(subset=required_columns)
        
        equipment_list = []
        for _, row in df.iterrows():
            equipment_list.append({
                'name': str(row['Equipment Name']).strip(),
                'type': str(row['Type']).strip(),
                'flowrate': float(row['Flowrate']),
                'pressure': float(row['Pressure']),
                'temperature': float(row['Temperature']),
            })
        
        return equipment_list, None
        
    except Exception as e:
        return None, str(e)


def calculate_summary(equipment_queryset):
    """
    Calculate summary statistics for equipment queryset.
    
    Args:
        equipment_queryset: QuerySet of Equipment objects
        
    Returns:
        dict: Summary statistics
    """
    stats = equipment_queryset.aggregate(
        total_count=Count('id'),
        avg_flowrate=Avg('flowrate'),
        avg_pressure=Avg('pressure'),
        avg_temperature=Avg('temperature'),
        min_flowrate=Min('flowrate'),
        max_flowrate=Max('flowrate'),
        min_pressure=Min('pressure'),
        max_pressure=Max('pressure'),
        min_temperature=Min('temperature'),
        max_temperature=Max('temperature'),
    )
    
    # Calculate type distribution
    type_counts = equipment_queryset.values('type').annotate(count=Count('id'))
    type_distribution = {item['type']: item['count'] for item in type_counts}
    
    # Handle None values for empty querysets
    for key in stats:
        if stats[key] is None:
            stats[key] = 0 if 'count' in key else 0.0
    
    stats['type_distribution'] = type_distribution
    
    return stats


def generate_pdf_report(equipment_queryset, summary, filename="report.pdf"):
    """
    Generate PDF report with equipment data and summary.
    
    Args:
        equipment_queryset: QuerySet of Equipment objects
        summary: Dict of summary statistics
        filename: Output filename
        
    Returns:
        BytesIO: PDF file buffer
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=50, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a365d'),
        spaceAfter=30,
        alignment=1  # Center
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c5282'),
        spaceBefore=20,
        spaceAfter=10
    )
    
    elements = []
    
    # Title
    elements.append(Paragraph("Chemical Equipment Analysis Report", title_style))
    elements.append(Spacer(1, 20))
    
    # Summary Section
    elements.append(Paragraph("Summary Statistics", heading_style))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Equipment Count', str(summary['total_count'])],
        ['Average Flowrate', f"{summary['avg_flowrate']:.2f}"],
        ['Average Pressure', f"{summary['avg_pressure']:.2f} bar"],
        ['Average Temperature', f"{summary['avg_temperature']:.2f} °C"],
        ['Flowrate Range', f"{summary['min_flowrate']:.2f} - {summary['max_flowrate']:.2f}"],
        ['Pressure Range', f"{summary['min_pressure']:.2f} - {summary['max_pressure']:.2f} bar"],
        ['Temperature Range', f"{summary['min_temperature']:.2f} - {summary['max_temperature']:.2f} °C"],
    ]
    
    summary_table = Table(summary_data, colWidths=[200, 200])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#edf2f7')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))
    
    # Type Distribution
    elements.append(Paragraph("Equipment Type Distribution", heading_style))
    
    type_data = [['Equipment Type', 'Count']]
    for eq_type, count in summary['type_distribution'].items():
        type_data.append([eq_type, str(count)])
    
    if len(type_data) > 1:
        type_table = Table(type_data, colWidths=[200, 100])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#38a169')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fff4')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#9ae6b4')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        elements.append(type_table)
    elements.append(Spacer(1, 30))
    
    # Equipment Data Table
    elements.append(Paragraph("Equipment Data", heading_style))
    
    equipment_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temp (°C)']]
    for eq in equipment_queryset[:50]:  # Limit to 50 for PDF readability
        equipment_data.append([
            eq.name,
            eq.type,
            f"{eq.flowrate:.1f}",
            f"{eq.pressure:.1f}",
            f"{eq.temperature:.1f}"
        ])
    
    eq_table = Table(equipment_data, colWidths=[100, 80, 70, 70, 70])
    eq_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#805ad5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#faf5ff')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d6bcfa')),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    elements.append(eq_table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
