"""
Upload Tab for PyQt5 Desktop Application.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class UploadTab(QWidget):
    """CSV file upload tab."""
    
    upload_success = pyqtSignal()
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.selected_file = None
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel('📤 Upload CSV Data')
        title.setStyleSheet('font-size: 20px; font-weight: bold; color: #f1f5f9;')
        layout.addWidget(title)
        
        # Drop zone
        self.drop_zone = QFrame()
        self.drop_zone.setObjectName('dropZone')
        self.drop_zone.setMinimumHeight(250)
        self.drop_zone.setStyleSheet('''
            #dropZone {
                background: #1e293b;
                border: 2px dashed #64748b;
                border-radius: 16px;
            }
            #dropZone:hover {
                border-color: #3b82f6;
                background: rgba(59, 130, 246, 0.1);
            }
        ''')
        
        drop_layout = QVBoxLayout(self.drop_zone)
        drop_layout.setAlignment(Qt.AlignCenter)
        
        self.file_icon = QLabel('📁')
        self.file_icon.setFont(QFont('Segoe UI Emoji', 48))
        self.file_icon.setAlignment(Qt.AlignCenter)
        drop_layout.addWidget(self.file_icon)
        
        self.file_label = QLabel('Click to select a CSV file')
        self.file_label.setStyleSheet('color: #94a3b8; font-size: 16px;')
        self.file_label.setAlignment(Qt.AlignCenter)
        drop_layout.addWidget(self.file_label)
        
        self.browse_btn = QPushButton('Browse Files')
        self.browse_btn.setStyleSheet('''
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #8b5cf6);
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb, stop:1 #7c3aed);
            }
        ''')
        self.browse_btn.clicked.connect(self.select_file)
        drop_layout.addWidget(self.browse_btn, alignment=Qt.AlignCenter)
        
        layout.addWidget(self.drop_zone)
        
        # Upload button
        self.upload_btn = QPushButton('🚀 Upload File')
        self.upload_btn.setEnabled(False)
        self.upload_btn.setStyleSheet('''
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10b981, stop:1 #06b6d4);
                border: none;
                border-radius: 8px;
                padding: 16px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #059669, stop:1 #0891b2);
            }
            QPushButton:disabled {
                background: #334155;
                color: #64748b;
            }
        ''')
        self.upload_btn.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_btn)
        
        # Status message
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
    
    def select_file(self):
        """Open file dialog to select CSV."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select CSV File', '', 'CSV Files (*.csv)'
        )
        
        if file_path:
            self.selected_file = file_path
            filename = file_path.split('/')[-1]
            self.file_icon.setText('📄')
            self.file_label.setText(filename)
            self.file_label.setStyleSheet('color: #10b981; font-size: 16px; font-weight: bold;')
            self.upload_btn.setEnabled(True)
            self.drop_zone.setStyleSheet('''
                #dropZone {
                    background: rgba(16, 185, 129, 0.1);
                    border: 2px solid #10b981;
                    border-radius: 16px;
                }
            ''')
    
    def upload_file(self):
        """Upload the selected file."""
        if not self.selected_file:
            return
        
        self.upload_btn.setEnabled(False)
        self.upload_btn.setText('Uploading...')
        self.status_label.setText('')
        
        success, data = self.api_client.upload_csv(self.selected_file)
        
        if success:
            count = data.get('equipment_count', 0)
            self.status_label.setStyleSheet('''
                color: #10b981;
                background: rgba(16, 185, 129, 0.15);
                border-radius: 8px;
                padding: 12px;
            ''')
            self.status_label.setText(f'✅ Successfully uploaded {count} equipment records')
            self.upload_success.emit()
            self.reset_form()
        else:
            error = data.get('error', 'Upload failed')
            self.status_label.setStyleSheet('''
                color: #ef4444;
                background: rgba(239, 68, 68, 0.15);
                border-radius: 8px;
                padding: 12px;
            ''')
            self.status_label.setText(f'❌ {error}')
            self.upload_btn.setEnabled(True)
        
        self.upload_btn.setText('🚀 Upload File')
    
    def reset_form(self):
        """Reset the upload form."""
        self.selected_file = None
        self.file_icon.setText('📁')
        self.file_label.setText('Click to select a CSV file')
        self.file_label.setStyleSheet('color: #94a3b8; font-size: 16px;')
        self.upload_btn.setEnabled(False)
        self.drop_zone.setStyleSheet('''
            #dropZone {
                background: #1e293b;
                border: 2px dashed #64748b;
                border-radius: 16px;
            }
            #dropZone:hover {
                border-color: #3b82f6;
                background: rgba(59, 130, 246, 0.1);
            }
        ''')
