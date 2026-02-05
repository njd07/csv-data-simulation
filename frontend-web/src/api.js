import axios from 'axios';

const API_BASE_URL = 'https://csv-data-simulation.onrender.com/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add auth token to requests if available
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
});

// Handle 401 responses
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/';
        }
        return Promise.reject(error);
    }
);

export const authAPI = {
    register: (data) => api.post('/auth/register/', data),
    login: (data) => api.post('/auth/login/', data),
};

export const dataAPI = {
    upload: (file) => {
        const formData = new FormData();
        formData.append('file', file);
        return api.post('/upload/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
    },
    getData: (uploadId = null) => {
        const params = uploadId ? { upload_id: uploadId } : {};
        return api.get('/data/', { params });
    },
    getSummary: (uploadId = null) => {
        const params = uploadId ? { upload_id: uploadId } : {};
        return api.get('/summary/', { params });
    },
    getHistory: () => api.get('/history/'),
    downloadReport: async (uploadId = null) => {
        const params = uploadId ? { upload_id: uploadId } : {};
        const response = await api.get('/report/', {
            params,
            responseType: 'blob'
        });
        const blob = new Blob([response.data], { type: 'application/pdf' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'equipment_report.pdf';
        link.click();
        window.URL.revokeObjectURL(url);
    },
};

export default api;
