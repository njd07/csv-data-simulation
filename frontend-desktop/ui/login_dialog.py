"""
Login Dialog for PyQt5 Desktop Application.
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QWidget, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class LoginDialog(QDialog):
    """Login/Register dialog window."""
    
    login_success = pyqtSignal(dict)
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """Initialize the UI components."""
        self.setWindowTitle('Chemical Equipment Analysis')
        self.setFixedSize(420, 480)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Main container
        container = QFrame()
        container.setObjectName('mainContainer')
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(20)
        
        # Header
        header = QLabel('⚗️')
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont('Segoe UI Emoji', 48))
        container_layout.addWidget(header)
        
        title = QLabel('Chemical Equipment')
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName('title')
        container_layout.addWidget(title)
        
        subtitle = QLabel('Analysis Platform')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName('subtitle')
        container_layout.addWidget(subtitle)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setObjectName('authTabs')
        
        # Login tab
        login_tab = QWidget()
        login_layout = QVBoxLayout(login_tab)
        login_layout.setSpacing(15)
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText('Username')
        login_layout.addWidget(self.login_username)
        
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText('Password')
        self.login_password.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(self.login_password)
        
        self.login_btn = QPushButton('Sign In')
        self.login_btn.setObjectName('primaryBtn')
        self.login_btn.clicked.connect(self.handle_login)
        login_layout.addWidget(self.login_btn)
        
        # Register tab
        register_tab = QWidget()
        register_layout = QVBoxLayout(register_tab)
        register_layout.setSpacing(15)
        
        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText('Username')
        register_layout.addWidget(self.reg_username)
        
        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText('Email (optional)')
        register_layout.addWidget(self.reg_email)
        
        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText('Password (min 6 characters)')
        self.reg_password.setEchoMode(QLineEdit.Password)
        register_layout.addWidget(self.reg_password)
        
        self.register_btn = QPushButton('Create Account')
        self.register_btn.setObjectName('primaryBtn')
        self.register_btn.clicked.connect(self.handle_register)
        register_layout.addWidget(self.register_btn)
        
        self.tabs.addTab(login_tab, 'Login')
        self.tabs.addTab(register_tab, 'Register')
        container_layout.addWidget(self.tabs)
        
        # Close button
        close_btn = QPushButton('Cancel')
        close_btn.setObjectName('secondaryBtn')
        close_btn.clicked.connect(self.reject)
        container_layout.addWidget(close_btn)
        
        layout.addWidget(container)
    
    def apply_styles(self):
        """Apply Qt stylesheet - Emerald Glass Theme."""
        self.setStyleSheet('''
            #mainContainer {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f172a, stop:0.5 #1e1b4b, stop:1 #0f172a);
                border-radius: 24px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            #title {
                color: #34d399;
                font-size: 26px;
                font-weight: bold;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            
            #subtitle {
                color: #94a3b8;
                font-size: 13px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            
            QLabel {
                color: #f1f5f9;
            }
            
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.03);
                color: #94a3b8;
                padding: 14px 35px;
                border-radius: 12px;
                margin: 3px;
                font-size: 13px;
                font-weight: 500;
                border: 1px solid rgba(255, 255, 255, 0.08);
            }
            
            QTabBar::tab:hover {
                background: rgba(255, 255, 255, 0.08);
                color: #f1f5f9;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10b981, stop:1 #14b8a6);
                color: white;
                border: none;
            }
            
            QLineEdit {
                background: rgba(15, 23, 42, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 16px 18px;
                color: #f1f5f9;
                font-size: 14px;
            }
            
            QLineEdit:focus {
                border-color: #10b981;
                border-width: 2px;
            }
            
            QLineEdit::placeholder {
                color: #64748b;
            }
            
            #primaryBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10b981, stop:1 #14b8a6);
                border: none;
                border-radius: 12px;
                padding: 16px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            
            #primaryBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #059669, stop:1 #0d9488);
            }
            
            #primaryBtn:disabled {
                background: #374151;
                color: #6b7280;
            }
            
            #secondaryBtn {
                background: transparent;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 10px;
                padding: 12px;
                color: #94a3b8;
                font-size: 13px;
            }
            
            #secondaryBtn:hover {
                background: rgba(255, 255, 255, 0.08);
                border-color: rgba(255, 255, 255, 0.25);
            }
        ''')
    
    def handle_login(self):
        """Handle login button click."""
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        self.login_btn.setEnabled(False)
        self.login_btn.setText('Signing in...')
        
        success, data = self.api_client.login(username, password)
        
        if success:
            self.login_success.emit(data['user'])
            self.accept()
        else:
            error = data.get('error', 'Login failed')
            QMessageBox.warning(self, 'Login Failed', error)
        
        self.login_btn.setEnabled(True)
        self.login_btn.setText('Sign In')
    
    def handle_register(self):
        """Handle register button click."""
        username = self.reg_username.text().strip()
        email = self.reg_email.text().strip()
        password = self.reg_password.text()
        
        if not username or len(password) < 6:
            QMessageBox.warning(self, 'Error', 'Username required and password must be at least 6 characters')
            return
        
        self.register_btn.setEnabled(False)
        self.register_btn.setText('Creating account...')
        
        success, data = self.api_client.register(username, password, email)
        
        if success:
            self.login_success.emit(data['user'])
            self.accept()
        else:
            error = data.get('error', 'Registration failed')
            if isinstance(error, dict):
                error = str(error)
            QMessageBox.warning(self, 'Registration Failed', error)
        
        self.register_btn.setEnabled(True)
        self.register_btn.setText('Create Account')
