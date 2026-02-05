"""
Charts Tab for PyQt5 Desktop Application.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class ChartsTab(QWidget):
    """Matplotlib charts tab."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []
        self.summary = {}
        self.setup_ui()
        
        # Set matplotlib dark style
        plt.style.use('dark_background')
    
    def setup_ui(self):
        """Initialize the UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title = QLabel('📈 Visualizations')
        title.setStyleSheet('font-size: 20px; font-weight: bold; color: #f1f5f9;')
        main_layout.addWidget(title)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet('''
            QScrollArea {
                background: transparent;
                border: none;
            }
        ''')
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(20)
        
        # Charts row
        charts_row = QHBoxLayout()
        
        # Pie chart container
        self.pie_container = QFrame()
        self.pie_container.setStyleSheet('''
            QFrame {
                background: #1e293b;
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
        ''')
        pie_layout = QVBoxLayout(self.pie_container)
        
        self.pie_figure = Figure(figsize=(5, 4), facecolor='#1e293b')
        self.pie_canvas = FigureCanvas(self.pie_figure)
        pie_layout.addWidget(self.pie_canvas)
        charts_row.addWidget(self.pie_container)
        
        # Bar chart container
        self.bar_container = QFrame()
        self.bar_container.setStyleSheet('''
            QFrame {
                background: #1e293b;
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
        ''')
        bar_layout = QVBoxLayout(self.bar_container)
        
        self.bar_figure = Figure(figsize=(5, 4), facecolor='#1e293b')
        self.bar_canvas = FigureCanvas(self.bar_figure)
        bar_layout.addWidget(self.bar_canvas)
        charts_row.addWidget(self.bar_container)
        
        scroll_layout.addLayout(charts_row)
        
        # Line chart container
        self.line_container = QFrame()
        self.line_container.setStyleSheet('''
            QFrame {
                background: #1e293b;
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
        ''')
        line_layout = QVBoxLayout(self.line_container)
        
        self.line_figure = Figure(figsize=(10, 4), facecolor='#1e293b')
        self.line_canvas = FigureCanvas(self.line_figure)
        line_layout.addWidget(self.line_canvas)
        scroll_layout.addWidget(self.line_container)
        
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # Empty state
        self.empty_label = QLabel('📉 No data available for visualization\nUpload a CSV file to see charts')
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet('color: #64748b; font-size: 16px;')
        main_layout.addWidget(self.empty_label)
        self.empty_label.hide()
    
    def set_data(self, data, summary):
        """Set chart data."""
        self.data = data if data else []
        self.summary = summary if summary else {}
        self.update_charts()
    
    def update_charts(self):
        """Update all charts."""
        if not self.data or not self.summary:
            self.pie_container.hide()
            self.bar_container.hide()
            self.line_container.hide()
            self.empty_label.show()
            return
        
        self.pie_container.show()
        self.bar_container.show()
        self.line_container.show()
        self.empty_label.hide()
        
        self.update_pie_chart()
        self.update_bar_chart()
        self.update_line_chart()
    
    def update_pie_chart(self):
        """Update the pie chart."""
        self.pie_figure.clear()
        ax = self.pie_figure.add_subplot(111)
        ax.set_facecolor('#1e293b')
        
        type_dist = self.summary.get('type_distribution', {})
        if type_dist:
            labels = list(type_dist.keys())
            values = list(type_dist.values())
            colors = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']
            
            wedges, texts, autotexts = ax.pie(
                values, labels=labels, autopct='%1.1f%%',
                colors=colors[:len(labels)],
                textprops={'color': '#e2e8f0'}
            )
            for autotext in autotexts:
                autotext.set_color('#1e293b')
                autotext.set_fontweight('bold')
            
            ax.set_title('Equipment Type Distribution', color='#e2e8f0', fontsize=14)
        
        self.pie_canvas.draw()
    
    def update_bar_chart(self):
        """Update the bar chart."""
        self.bar_figure.clear()
        ax = self.bar_figure.add_subplot(111)
        ax.set_facecolor('#1e293b')
        
        # Sort by flowrate and take top 10
        sorted_data = sorted(self.data, key=lambda x: x.get('flowrate', 0), reverse=True)[:10]
        
        if sorted_data:
            names = [d.get('name', '')[:10] for d in sorted_data]
            flowrates = [d.get('flowrate', 0) for d in sorted_data]
            
            bars = ax.bar(names, flowrates, color='#6366f1', edgecolor='#818cf8', linewidth=1)
            ax.set_xlabel('Equipment', color='#a0aec0')
            ax.set_ylabel('Flowrate', color='#a0aec0')
            ax.set_title('Top 10 Equipment by Flowrate', color='#e2e8f0', fontsize=14)
            ax.tick_params(colors='#a0aec0', rotation=45)
            ax.grid(True, alpha=0.1)
            
            # Add value labels
            for bar, val in zip(bars, flowrates):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                       f'{val:.0f}', ha='center', va='bottom', color='#e2e8f0', fontsize=8)
        
        self.bar_figure.tight_layout()
        self.bar_canvas.draw()
    
    def update_line_chart(self):
        """Update the line chart."""
        self.line_figure.clear()
        ax = self.line_figure.add_subplot(111)
        ax.set_facecolor('#1e293b')
        
        if self.data:
            names = [d.get('name', '')[:8] for d in self.data]
            pressures = [d.get('pressure', 0) for d in self.data]
            temperatures = [d.get('temperature', 0) for d in self.data]
            
            ax.plot(names, pressures, 'o-', color='#10b981', label='Pressure (bar)', linewidth=2, markersize=6)
            ax.plot(names, temperatures, 's-', color='#ef4444', label='Temperature (°C)', linewidth=2, markersize=6)
            
            ax.fill_between(names, pressures, alpha=0.2, color='#10b981')
            ax.fill_between(names, temperatures, alpha=0.2, color='#ef4444')
            
            ax.set_xlabel('Equipment', color='#a0aec0')
            ax.set_title('Pressure vs Temperature Comparison', color='#e2e8f0', fontsize=14)
            ax.tick_params(colors='#a0aec0', rotation=45)
            ax.legend(facecolor='#334155', labelcolor='#e2e8f0')
            ax.grid(True, alpha=0.1)
        
        self.line_figure.tight_layout()
        self.line_canvas.draw()
