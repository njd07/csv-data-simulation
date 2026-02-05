"""
History Tab for PyQt5 Desktop Application.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea, QHBoxLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from datetime import datetime


class HistoryTab(QWidget):
    """Upload history tab."""
    
    upload_selected = pyqtSignal(object)  # None or upload_id
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.history = []
        self.selected_id = None
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel('📚 Upload History')
        title.setStyleSheet('font-size: 20px; font-weight: bold; color: #f1f5f9;')
        layout.addWidget(title)
        
        subtitle = QLabel('Last 5 uploads (click to view)')
        subtitle.setStyleSheet('color: #64748b; font-size: 13px;')
        layout.addWidget(subtitle)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet('QScrollArea { background: transparent; border: none; }')
        
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        
        scroll.setWidget(self.scroll_widget)
        layout.addWidget(scroll)
        
        # Empty state
        self.empty_label = QLabel('📂 No upload history\nYour recent uploads will appear here')
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet('color: #64748b; font-size: 16px;')
        layout.addWidget(self.empty_label)
    
    def set_history(self, history):
        """Update history data."""
        self.history = history if history else []
        self.update_display()
    
    def update_display(self):
        """Update the display."""
        # Clear existing items
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.history:
            self.empty_label.show()
            return
        
        self.empty_label.hide()
        
        for upload in self.history:
            item = self.create_history_item(upload)
            self.scroll_layout.addWidget(item)
        
        self.scroll_layout.addStretch()
    
    def create_history_item(self, upload):
        """Create a history item widget."""
        upload_id = upload.get('id')
        is_selected = upload_id == self.selected_id
        
        item = QFrame()
        item.setObjectName('historyItem')
        item.setCursor(Qt.PointingHandCursor)
        
        border_style = 'border: 2px solid #10b981;' if is_selected else 'border: 1px solid rgba(255, 255, 255, 0.08);'
        bg_style = 'background: rgba(16, 185, 129, 0.15);' if is_selected else 'background: rgba(30, 41, 59, 0.8);'
        
        item.setStyleSheet(f'''
            #historyItem {{
                {bg_style}
                {border_style}
                border-radius: 14px;
                padding: 15px;
            }}
            #historyItem:hover {{
                background: rgba(16, 185, 129, 0.08);
                border-color: rgba(16, 185, 129, 0.4);
            }}
        ''')
        
        layout = QHBoxLayout(item)
        layout.setSpacing(15)
        
        # File icon
        icon = QLabel('📄')
        icon.setStyleSheet('font-size: 28px;')
        layout.addWidget(icon)
        
        # Info
        info_layout = QVBoxLayout()
        
        filename = QLabel(upload.get('filename', 'Unknown'))
        filename.setStyleSheet('color: #f1f5f9; font-weight: bold; font-size: 14px;')
        info_layout.addWidget(filename)
        
        date_str = upload.get('uploaded_at', '')
        if date_str:
            try:
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                formatted_date = dt.strftime('%b %d, %Y at %H:%M')
            except:
                formatted_date = date_str
        else:
            formatted_date = 'Unknown date'
        
        date_label = QLabel(formatted_date)
        date_label.setStyleSheet('color: #64748b; font-size: 12px;')
        info_layout.addWidget(date_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Record count
        count_frame = QFrame()
        count_frame.setStyleSheet('''
            QFrame {
                background: rgba(16, 185, 129, 0.15);
                border-radius: 10px;
                padding: 10px 14px;
            }
        ''')
        count_layout = QVBoxLayout(count_frame)
        count_layout.setContentsMargins(0, 0, 0, 0)
        count_layout.setSpacing(2)
        
        count_value = QLabel(str(upload.get('record_count', 0)))
        count_value.setStyleSheet('color: #34d399; font-size: 20px; font-weight: bold;')
        count_value.setAlignment(Qt.AlignCenter)
        count_layout.addWidget(count_value)
        
        count_label = QLabel('RECORDS')
        count_label.setStyleSheet('color: #64748b; font-size: 9px;')
        count_label.setAlignment(Qt.AlignCenter)
        count_layout.addWidget(count_label)
        
        layout.addWidget(count_frame)
        
        # Selected indicator
        if is_selected:
            check = QLabel('✓')
            check.setStyleSheet('''
                background: #10b981;
                color: white;
                border-radius: 12px;
                padding: 4px 8px;
                font-weight: bold;
            ''')
            layout.addWidget(check)
        
        # Click handler
        item.mousePressEvent = lambda e, uid=upload_id: self.on_item_clicked(uid)
        
        return item
    
    def on_item_clicked(self, upload_id):
        """Handle item click."""
        if self.selected_id == upload_id:
            self.selected_id = None
            self.upload_selected.emit(None)
        else:
            self.selected_id = upload_id
            self.upload_selected.emit(upload_id)
        
        self.update_display()
