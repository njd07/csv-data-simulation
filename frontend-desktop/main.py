"""
Chemical Equipment Analysis - PyQt5 Desktop Application
Main entry point with main window implementation.
"""
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTabWidget, QFrame, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from api_client import api_client
from ui.login_dialog import LoginDialog
from ui.upload_tab import UploadTab
from ui.data_tab import DataTab
from ui.charts_tab import ChartsTab
from ui.summary_tab import SummaryTab
from ui.history_tab import HistoryTab


class DataLoader(QThread):
    """Background thread for loading data."""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, upload_id=None):
        super().__init__()
        self.upload_id = upload_id
    
    def run(self):
        try:
            data_success, data = api_client.get_data(self.upload_id)
            summary_success, summary = api_client.get_summary(self.upload_id)
            history_success, history = api_client.get_history()
            
            self.finished.emit({
                'data': data if data_success else [],
                'summary': summary if summary_success else {},
                'history': history if history_success else []
            })
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.user = None
        self.selected_upload_id = None
        self.loader = None
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """Initialize the main UI."""
        self.setWindowTitle('Chemical Equipment Analysis')
        self.setMinimumSize(1200, 800)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setObjectName('header')
        header.setFixedHeight(70)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        # Logo and brand
        logo = QLabel('⚗️')
        logo.setFont(QFont('Segoe UI Emoji', 28))
        header_layout.addWidget(logo)
        
        brand_layout = QVBoxLayout()
        brand_layout.setSpacing(0)
        brand_title = QLabel('Chemical Equipment')
        brand_title.setObjectName('brandTitle')
        brand_layout.addWidget(brand_title)
        brand_sub = QLabel('Analysis Platform')
        brand_sub.setObjectName('brandSub')
        brand_layout.addWidget(brand_sub)
        header_layout.addLayout(brand_layout)
        
        header_layout.addStretch()
        
        # PDF button
        self.pdf_btn = QPushButton('📥 PDF Report')
        self.pdf_btn.setObjectName('pdfBtn')
        self.pdf_btn.clicked.connect(self.download_pdf)
        header_layout.addWidget(self.pdf_btn)
        
        # User info
        self.user_label = QLabel('👤 Guest')
        self.user_label.setObjectName('userLabel')
        header_layout.addWidget(self.user_label)
        
        # Logout button
        self.logout_btn = QPushButton('Logout')
        self.logout_btn.setObjectName('logoutBtn')
        self.logout_btn.clicked.connect(self.logout)
        header_layout.addWidget(self.logout_btn)
        
        main_layout.addWidget(header)
        
        # Content area
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Sidebar (History)
        sidebar = QFrame()
        sidebar.setObjectName('sidebar')
        sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        self.history_tab = HistoryTab()
        self.history_tab.upload_selected.connect(self.on_upload_selected)
        sidebar_layout.addWidget(self.history_tab)
        
        content_layout.addWidget(sidebar)
        
        # Main tabs
        self.tabs = QTabWidget()
        self.tabs.setObjectName('mainTabs')
        
        # Dashboard tab (Summary + Charts)
        dashboard_widget = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_widget)
        self.summary_widget = SummaryTab()
        dashboard_layout.addWidget(self.summary_widget)
        self.tabs.addTab(dashboard_widget, '📊 Dashboard')
        
        # Upload tab
        self.upload_tab = UploadTab(api_client)
        self.upload_tab.upload_success.connect(self.refresh_data)
        self.tabs.addTab(self.upload_tab, '📤 Upload')
        
        # Data tab
        self.data_tab = DataTab()
        self.tabs.addTab(self.data_tab, '📋 Data')
        
        # Charts tab
        self.charts_tab = ChartsTab()
        self.tabs.addTab(self.charts_tab, '📈 Charts')
        
        content_layout.addWidget(self.tabs)
        main_layout.addWidget(content)
        
        # Footer
        footer = QFrame()
        footer.setObjectName('footer')
        footer.setFixedHeight(40)
        footer_layout = QHBoxLayout(footer)
        
        footer_text = QLabel('Chemical Equipment Analysis Platform © 2026 | Built with Django + PyQt5')
        footer_text.setAlignment(Qt.AlignCenter)
        footer_text.setObjectName('footerText')
        footer_layout.addWidget(footer_text)
        
        main_layout.addWidget(footer)
    
    def apply_styles(self):
        """Apply application stylesheet - Emerald Glass Theme."""
        self.setStyleSheet('''
            /* Main Window */
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f172a, stop:0.5 #1e1b4b, stop:1 #0f172a);
            }
            
            /* Header */
            #header {
                background: rgba(15, 23, 42, 0.95);
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            }
            
            #brandTitle {
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #34d399, stop:1 #14b8a6);
                color: #34d399;
                font-size: 20px;
                font-weight: bold;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            
            #brandSub {
                color: #94a3b8;
                font-size: 11px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            
            /* PDF Button - Emerald Gradient */
            #pdfBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10b981, stop:1 #14b8a6);
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                color: white;
                font-weight: bold;
                font-size: 13px;
            }
            
            #pdfBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #059669, stop:1 #0d9488);
            }
            
            #pdfBtn:disabled {
                background: #374151;
                color: #6b7280;
            }
            
            /* User Label */
            #userLabel {
                color: #e2e8f0;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 25px;
                padding: 10px 20px;
                font-size: 13px;
            }
            
            /* Logout Button */
            #logoutBtn {
                background: transparent;
                border: 1px solid rgba(244, 63, 94, 0.4);
                border-radius: 10px;
                padding: 10px 20px;
                color: #fca5a5;
                font-size: 12px;
            }
            
            #logoutBtn:hover {
                background: rgba(244, 63, 94, 0.1);
                border-color: #f43f5e;
            }
            
            /* Sidebar */
            #sidebar {
                background: rgba(30, 41, 59, 0.7);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.08);
            }
            
            /* Main Tabs */
            #mainTabs {
                background: transparent;
            }
            
            #mainTabs::pane {
                background: rgba(30, 41, 59, 0.7);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.08);
                padding: 15px;
            }
            
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.03);
                color: #94a3b8;
                padding: 14px 28px;
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
            
            /* Footer */
            #footer {
                background: rgba(15, 23, 42, 0.8);
                border-top: 1px solid rgba(255, 255, 255, 0.05);
            }
            
            #footerText {
                color: #64748b;
                font-size: 12px;
            }
            
            /* All Labels - Default styling */
            QLabel {
                color: #f1f5f9;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            
            /* Frames/Cards */
            QFrame {
                background: transparent;
            }
            
            /* Buttons */
            QPushButton {
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            
            /* Tables */
            QTableWidget {
                background: rgba(15, 23, 42, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                gridline-color: rgba(255, 255, 255, 0.05);
                color: #f1f5f9;
                selection-background-color: rgba(16, 185, 129, 0.3);
            }
            
            QTableWidget::item {
                padding: 12px 15px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }
            
            QTableWidget::item:hover {
                background: rgba(16, 185, 129, 0.08);
            }
            
            QTableWidget::item:selected {
                background: rgba(16, 185, 129, 0.2);
            }
            
            QHeaderView::section {
                background: rgba(16, 185, 129, 0.15);
                color: #34d399;
                padding: 14px 15px;
                border: none;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                font-weight: bold;
                font-size: 11px;
                text-transform: uppercase;
            }
            
            /* Scrollbars */
            QScrollBar:vertical {
                background: #1e293b;
                width: 10px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical {
                background: #334155;
                border-radius: 5px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #10b981;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar:horizontal {
                background: #1e293b;
                height: 10px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:horizontal {
                background: #334155;
                border-radius: 5px;
                min-width: 30px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: #10b981;
            }
            
            /* Line Edits */
            QLineEdit {
                background: rgba(15, 23, 42, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 12px 16px;
                color: #f1f5f9;
                font-size: 14px;
                selection-background-color: #10b981;
            }
            
            QLineEdit:focus {
                border-color: #10b981;
            }
            
            QLineEdit::placeholder {
                color: #64748b;
            }
            
            /* Combo Boxes */
            QComboBox {
                background: rgba(15, 23, 42, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 10px 14px;
                color: #f1f5f9;
                min-width: 120px;
            }
            
            QComboBox:hover {
                border-color: #10b981;
            }
            
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            
            QComboBox QAbstractItemView {
                background: #1e293b;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                selection-background-color: #10b981;
            }
            
            /* Tool Tips */
            QToolTip {
                background: #1e293b;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 8px 12px;
                color: #f1f5f9;
            }
            
            /* Message Boxes */
            QMessageBox {
                background: #1e293b;
            }
            
            QMessageBox QLabel {
                color: #f1f5f9;
            }
            
            QMessageBox QPushButton {
                background: #10b981;
                border: none;
                border-radius: 8px;
                padding: 10px 25px;
                color: white;
                min-width: 80px;
            }
            
            QMessageBox QPushButton:hover {
                background: #059669;
            }
        ''')
    
    def show_login(self):
        """Show the login dialog."""
        dialog = LoginDialog(api_client, self)
        dialog.login_success.connect(self.on_login_success)
        dialog.exec_()
        
        if not api_client.is_authenticated():
            sys.exit(0)
    
    def on_login_success(self, user):
        """Handle successful login."""
        self.user = user
        self.user_label.setText(f"👤 {user.get('username', 'User')}")
        self.refresh_data()
    
    def on_upload_selected(self, upload_id):
        """Handle upload selection from history."""
        self.selected_upload_id = upload_id
        self.refresh_data()
    
    def refresh_data(self):
        """Refresh all data from API."""
        if self.loader and self.loader.isRunning():
            return
        
        self.loader = DataLoader(self.selected_upload_id)
        self.loader.finished.connect(self.on_data_loaded)
        self.loader.error.connect(self.on_data_error)
        self.loader.start()
    
    def on_data_loaded(self, result):
        """Handle loaded data."""
        data = result.get('data', [])
        summary = result.get('summary', {})
        history = result.get('history', [])
        
        self.data_tab.set_data(data)
        self.charts_tab.set_data(data, summary)
        self.summary_widget.set_summary(summary)
        self.history_tab.set_history(history)
    
    def on_data_error(self, error):
        """Handle data loading error."""
        QMessageBox.warning(self, 'Error', f'Failed to load data: {error}')
    
    def download_pdf(self):
        """Download PDF report."""
        success, content = api_client.download_report(self.selected_upload_id)
        
        if success and content:
            file_path, _ = QFileDialog.getSaveFileName(
                self, 'Save PDF Report', 'equipment_report.pdf', 'PDF Files (*.pdf)'
            )
            if file_path:
                with open(file_path, 'wb') as f:
                    f.write(content)
                QMessageBox.information(self, 'Success', 'PDF report saved successfully!')
        else:
            QMessageBox.warning(self, 'Error', 'Failed to generate PDF report. Make sure you have data uploaded.')
    
    def logout(self):
        """Log out the user."""
        api_client.clear_token()
        self.user = None
        self.user_label.setText('👤 Guest')
        self.show_login()


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application font
    font = QFont('Segoe UI', 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    window.show_login()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
