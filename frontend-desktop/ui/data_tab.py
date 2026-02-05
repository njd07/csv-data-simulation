"""
Data Tab for PyQt5 Desktop Application.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QLineEdit, QPushButton, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class DataTab(QWidget):
    """Equipment data table tab."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []
        self.filtered_data = []
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QHBoxLayout()
        
        title = QLabel('📊 Equipment Data')
        title.setStyleSheet('font-size: 20px; font-weight: bold; color: #f1f5f9;')
        header.addWidget(title)
        
        header.addStretch()
        
        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('🔍 Search equipment...')
        self.search_input.setFixedWidth(250)
        self.search_input.setStyleSheet('''
            QLineEdit {
                background: #334155;
                border: 2px solid transparent;
                border-radius: 8px;
                padding: 10px 15px;
                color: #f1f5f9;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
        ''')
        self.search_input.textChanged.connect(self.filter_data)
        header.addWidget(self.search_input)
        
        layout.addLayout(header)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Name', 'Type', 'Flowrate', 'Pressure (bar)', 'Temp (°C)'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSortingEnabled(True)
        self.table.setStyleSheet('''
            QTableWidget {
                background: #1e293b;
                border: none;
                border-radius: 8px;
                gridline-color: rgba(255, 255, 255, 0.05);
                color: #f1f5f9;
            }
            QTableWidget::item {
                padding: 12px;
            }
            QTableWidget::item:selected {
                background: rgba(59, 130, 246, 0.3);
            }
            QTableWidget::item:alternate {
                background: rgba(255, 255, 255, 0.02);
            }
            QHeaderView::section {
                background: #334155;
                color: #f1f5f9;
                padding: 12px;
                border: none;
                font-weight: bold;
            }
        ''')
        layout.addWidget(self.table)
        
        # Status bar
        self.status_label = QLabel('No data loaded')
        self.status_label.setStyleSheet('color: #64748b; font-size: 13px;')
        layout.addWidget(self.status_label)
    
    def set_data(self, data):
        """Set the equipment data."""
        self.data = data if data else []
        self.filter_data()
    
    def filter_data(self):
        """Filter data based on search term."""
        search = self.search_input.text().lower()
        
        if search:
            self.filtered_data = [
                item for item in self.data
                if search in item.get('name', '').lower() or
                   search in item.get('type', '').lower()
            ]
        else:
            self.filtered_data = self.data
        
        self.update_table()
    
    def update_table(self):
        """Update the table with filtered data."""
        self.table.setRowCount(len(self.filtered_data))
        
        for row, item in enumerate(self.filtered_data):
            # Name
            name_item = QTableWidgetItem(item.get('name', ''))
            name_item.setForeground(QColor('#3b82f6'))
            self.table.setItem(row, 0, name_item)
            
            # Type
            type_text = item.get('type', '')
            type_item = QTableWidgetItem(type_text)
            type_colors = {
                'Pump': '#93c5fd',
                'Compressor': '#c4b5fd',
                'Valve': '#fcd34d',
                'HeatExchanger': '#fca5a5',
                'Reactor': '#6ee7b7',
                'Condenser': '#67e8f9'
            }
            type_item.setForeground(QColor(type_colors.get(type_text, '#f1f5f9')))
            self.table.setItem(row, 1, type_item)
            
            # Numeric values
            for col, key in enumerate(['flowrate', 'pressure', 'temperature'], start=2):
                value = item.get(key, 0)
                value_item = QTableWidgetItem(f'{value:.2f}' if isinstance(value, float) else str(value))
                value_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, value_item)
        
        total = len(self.data)
        showing = len(self.filtered_data)
        if total == showing:
            self.status_label.setText(f'Showing all {total} records')
        else:
            self.status_label.setText(f'Showing {showing} of {total} records')
