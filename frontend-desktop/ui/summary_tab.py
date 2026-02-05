"""
Summary Tab for PyQt5 Desktop Application.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt


class SummaryTab(QWidget):
    """Summary statistics tab."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.summary = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Title
        title = QLabel('📋 Summary Statistics')
        title.setStyleSheet('font-size: 20px; font-weight: bold; color: #f1f5f9;')
        main_layout.addWidget(title)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet('QScrollArea { background: transparent; border: none; }')
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(20)
        
        # Stats cards grid
        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(15)
        scroll_layout.addLayout(self.stats_grid)
        
        # Ranges section
        self.ranges_frame = QFrame()
        self.ranges_frame.setStyleSheet('''
            QFrame {
                background: #1e293b;
                border-radius: 12px;
                padding: 15px;
            }
        ''')
        self.ranges_layout = QVBoxLayout(self.ranges_frame)
        scroll_layout.addWidget(self.ranges_frame)
        
        # Type distribution section
        self.types_frame = QFrame()
        self.types_frame.setStyleSheet('''
            QFrame {
                background: #1e293b;
                border-radius: 12px;
                padding: 15px;
            }
        ''')
        self.types_layout = QVBoxLayout(self.types_frame)
        scroll_layout.addWidget(self.types_frame)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # Empty state
        self.empty_label = QLabel('📊 No summary available\nUpload data to see statistics')
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet('color: #64748b; font-size: 16px;')
        main_layout.addWidget(self.empty_label)
    
    def set_summary(self, summary):
        """Update summary data."""
        self.summary = summary if summary else {}
        self.update_display()
    
    def update_display(self):
        """Update the display."""
        # Clear existing widgets
        while self.stats_grid.count():
            item = self.stats_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        while self.ranges_layout.count():
            item = self.ranges_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        while self.types_layout.count():
            item = self.types_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.summary or self.summary.get('total_count', 0) == 0:
            self.ranges_frame.hide()
            self.types_frame.hide()
            self.empty_label.show()
            return
        
        self.ranges_frame.show()
        self.types_frame.show()
        self.empty_label.hide()
        
        # Stats cards
        stats = [
            ('🔧', 'Total Equipment', str(self.summary.get('total_count', 0)), '#3b82f6'),
            ('💧', 'Avg Flowrate', f"{self.summary.get('avg_flowrate', 0):.2f}", '#06b6d4'),
            ('⚡', 'Avg Pressure', f"{self.summary.get('avg_pressure', 0):.2f} bar", '#10b981'),
            ('🌡️', 'Avg Temperature', f"{self.summary.get('avg_temperature', 0):.1f}°C", '#f59e0b'),
        ]
        
        for idx, (icon, label, value, color) in enumerate(stats):
            card = self.create_stat_card(icon, label, value, color)
            self.stats_grid.addWidget(card, 0, idx)
        
        # Ranges section
        ranges_title = QLabel('📏 Value Ranges')
        ranges_title.setStyleSheet('color: #94a3b8; font-size: 16px; font-weight: bold; margin-bottom: 10px;')
        self.ranges_layout.addWidget(ranges_title)
        
        ranges_grid = QGridLayout()
        ranges_grid.setSpacing(10)
        
        ranges = [
            ('💧', 'Flowrate', self.summary.get('min_flowrate', 0), self.summary.get('max_flowrate', 0)),
            ('⚡', 'Pressure (bar)', self.summary.get('min_pressure', 0), self.summary.get('max_pressure', 0)),
            ('🌡️', 'Temperature (°C)', self.summary.get('min_temperature', 0), self.summary.get('max_temperature', 0)),
        ]
        
        for idx, (icon, label, min_val, max_val) in enumerate(ranges):
            range_card = self.create_range_card(icon, label, min_val, max_val)
            ranges_grid.addWidget(range_card, 0, idx)
        
        self.ranges_layout.addLayout(ranges_grid)
        
        # Type distribution
        types_title = QLabel('🏭 Equipment Types')
        types_title.setStyleSheet('color: #94a3b8; font-size: 16px; font-weight: bold; margin-bottom: 10px;')
        self.types_layout.addWidget(types_title)
        
        types_row = QHBoxLayout()
        type_dist = self.summary.get('type_distribution', {})
        
        type_colors = {
            'Pump': '#93c5fd', 'Compressor': '#c4b5fd', 'Valve': '#fcd34d',
            'HeatExchanger': '#fca5a5', 'Reactor': '#6ee7b7', 'Condenser': '#67e8f9'
        }
        
        for eq_type, count in type_dist.items():
            type_badge = QFrame()
            type_badge.setStyleSheet(f'''
                QFrame {{
                    background: #334155;
                    border-radius: 8px;
                    padding: 8px 16px;
                    border-left: 4px solid {type_colors.get(eq_type, '#94a3b8')};
                }}
            ''')
            badge_layout = QHBoxLayout(type_badge)
            badge_layout.setSpacing(10)
            
            type_label = QLabel(eq_type)
            type_label.setStyleSheet(f'color: {type_colors.get(eq_type, "#f1f5f9")}; font-weight: bold;')
            badge_layout.addWidget(type_label)
            
            count_label = QLabel(str(count))
            count_label.setStyleSheet('color: #f1f5f9; font-size: 18px; font-weight: bold;')
            badge_layout.addWidget(count_label)
            
            types_row.addWidget(type_badge)
        
        types_row.addStretch()
        self.types_layout.addLayout(types_row)
    
    def create_stat_card(self, icon, label, value, color):
        """Create a statistics card."""
        card = QFrame()
        card.setStyleSheet(f'''
            QFrame {{
                background: #1e293b;
                border-radius: 12px;
                border-left: 4px solid {color};
                padding: 15px;
            }}
        ''')
        
        layout = QHBoxLayout(card)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet('font-size: 32px;')
        layout.addWidget(icon_label)
        
        info_layout = QVBoxLayout()
        
        label_lbl = QLabel(label)
        label_lbl.setStyleSheet('color: #94a3b8; font-size: 12px;')
        info_layout.addWidget(label_lbl)
        
        value_lbl = QLabel(value)
        value_lbl.setStyleSheet('color: #f1f5f9; font-size: 24px; font-weight: bold;')
        info_layout.addWidget(value_lbl)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        return card
    
    def create_range_card(self, icon, label, min_val, max_val):
        """Create a range display card."""
        card = QFrame()
        card.setStyleSheet('''
            QFrame {
                background: #334155;
                border-radius: 8px;
                padding: 12px;
            }
        ''')
        
        layout = QHBoxLayout(card)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet('font-size: 24px;')
        layout.addWidget(icon_label)
        
        info_layout = QVBoxLayout()
        
        label_lbl = QLabel(label)
        label_lbl.setStyleSheet('color: #94a3b8; font-size: 12px;')
        info_layout.addWidget(label_lbl)
        
        range_lbl = QLabel(f'{min_val:.2f} → {max_val:.2f}')
        range_lbl.setStyleSheet('color: #f1f5f9; font-size: 14px;')
        info_layout.addWidget(range_lbl)
        
        layout.addLayout(info_layout)
        
        return card
