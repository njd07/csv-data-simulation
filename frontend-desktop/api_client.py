"""
API Client for PyQt5 Desktop Application.
Handles all HTTP requests to the Django backend.
"""
import requests
from typing import Optional, Dict, Any, Tuple

API_BASE_URL = 'http://localhost:8000/api'


class APIClient:
    """HTTP client for backend API communication."""
    
    def __init__(self):
        self.token: Optional[str] = None
        self.user: Optional[Dict] = None
        self.session = requests.Session()
    
    def set_token(self, token: str, user: Dict):
        """Set authentication token."""
        self.token = token
        self.user = user
        self.session.headers['Authorization'] = f'Token {token}'
    
    def clear_token(self):
        """Clear authentication."""
        self.token = None
        self.user = None
        self.session.headers.pop('Authorization', None)
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.token is not None
    
    def register(self, username: str, password: str, email: str = '') -> Tuple[bool, Dict]:
        """Register a new user."""
        try:
            response = self.session.post(
                f'{API_BASE_URL}/auth/register/',
                json={'username': username, 'password': password, 'email': email}
            )
            if response.status_code == 201:
                data = response.json()
                self.set_token(data['token'], data['user'])
                return True, data
            return False, response.json()
        except Exception as e:
            return False, {'error': str(e)}
    
    def login(self, username: str, password: str) -> Tuple[bool, Dict]:
        """Authenticate user."""
        try:
            response = self.session.post(
                f'{API_BASE_URL}/auth/login/',
                json={'username': username, 'password': password}
            )
            if response.status_code == 200:
                data = response.json()
                self.set_token(data['token'], data['user'])
                return True, data
            return False, response.json()
        except Exception as e:
            return False, {'error': str(e)}
    
    def upload_csv(self, file_path: str) -> Tuple[bool, Dict]:
        """Upload a CSV file."""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.split('/')[-1], f, 'text/csv')}
                headers = {'Authorization': f'Token {self.token}'}
                response = requests.post(
                    f'{API_BASE_URL}/upload/',
                    files=files,
                    headers=headers
                )
            if response.status_code == 201:
                return True, response.json()
            return False, response.json()
        except Exception as e:
            return False, {'error': str(e)}
    
    def get_data(self, upload_id: Optional[int] = None) -> Tuple[bool, Any]:
        """Get equipment data."""
        try:
            params = {'upload_id': upload_id} if upload_id else {}
            response = self.session.get(f'{API_BASE_URL}/data/', params=params)
            if response.status_code == 200:
                return True, response.json()
            return False, response.json()
        except Exception as e:
            return False, {'error': str(e)}
    
    def get_summary(self, upload_id: Optional[int] = None) -> Tuple[bool, Dict]:
        """Get summary statistics."""
        try:
            params = {'upload_id': upload_id} if upload_id else {}
            response = self.session.get(f'{API_BASE_URL}/summary/', params=params)
            if response.status_code == 200:
                return True, response.json()
            return False, response.json()
        except Exception as e:
            return False, {'error': str(e)}
    
    def get_history(self) -> Tuple[bool, Any]:
        """Get upload history."""
        try:
            response = self.session.get(f'{API_BASE_URL}/history/')
            if response.status_code == 200:
                return True, response.json()
            return False, response.json()
        except Exception as e:
            return False, {'error': str(e)}
    
    def download_report(self, upload_id: Optional[int] = None) -> Tuple[bool, bytes]:
        """Download PDF report."""
        try:
            params = {'upload_id': upload_id} if upload_id else {}
            response = self.session.get(f'{API_BASE_URL}/report/', params=params)
            if response.status_code == 200:
                return True, response.content
            return False, b''
        except Exception as e:
            return False, b''


# Global API client instance
api_client = APIClient()
