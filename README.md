# Chemical Equipment Analysis Platform

A full-stack application for uploading, analyzing, and visualizing chemical equipment data.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Django](https://img.shields.io/badge/Django-4.2+-green)
![React](https://img.shields.io/badge/React-18+-61DAFB)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-41CD52)

## 🎯 Features

- **CSV Upload** - Upload equipment data via Web or Desktop interface
- **Data Analysis** - Automatic calculation of summary statistics
- **Visualizations** - Interactive charts (Pie, Bar, Line)
- **PDF Reports** - Generate downloadable reports
- **History Management** - Track last 5 uploaded datasets
- **Authentication** - Token-based user authentication

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐
│   React Web     │     │  PyQt5 Desktop  │
│   (Chart.js)    │     │  (Matplotlib)   │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │   Django REST API    │
          │   (DRF + SQLite)     │
          └─────────────────────┘
```

## 📁 Project Structure

```
├── backend/                 # Django REST API
│   ├── config/             # Django settings
│   ├── api/                # API app (models, views, serializers)
│   ├── manage.py
│   └── requirements.txt
├── frontend-web/           # React + Vite application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.jsx
│   │   └── api.js
│   └── package.json
├── frontend-desktop/       # PyQt5 application
│   ├── ui/                 # UI modules
│   ├── main.py
│   ├── api_client.py
│   └── requirements.txt
└── sample_equipment_data.csv
```

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations api
python manage.py migrate

# Start server
python manage.py runserver 8000
```

The API will be available at `http://localhost:8000/api/`

### 2. React Web Frontend

```bash
cd frontend-web

# Install dependencies
npm install

# Start development server
npm run dev
```

Open `http://localhost:5173` in your browser.

### 3. PyQt5 Desktop Application

```bash
cd frontend-desktop

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 📊 Sample Data

A sample CSV file is provided for testing:

| Equipment Name | Type | Flowrate | Pressure | Temperature |
|---------------|------|----------|----------|-------------|
| Pump-1 | Pump | 120 | 5.2 | 110 |
| Compressor-1 | Compressor | 95 | 8.4 | 95 |
| Valve-1 | Valve | 60 | 4.1 | 105 |
| ... | ... | ... | ... | ... |

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | User registration |
| `/api/auth/login/` | POST | User login (get token) |
| `/api/upload/` | POST | Upload CSV file |
| `/api/data/` | GET | Get equipment data |
| `/api/summary/` | GET | Get summary statistics |
| `/api/history/` | GET | Get upload history (last 5) |
| `/api/report/` | GET | Download PDF report |

## 🔐 Authentication

All data endpoints require a valid token. Include it in requests:

```
Authorization: Token <your-token>
```

## 🎨 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 4.2 + Django REST Framework |
| Database | SQLite |
| Web Frontend | React 18 + Vite + Chart.js |
| Desktop Frontend | PyQt5 + Matplotlib |
| Data Processing | Pandas |
| PDF Generation | ReportLab |

## 📝 License

MIT License - feel free to use for educational purposes.

---

Built with ❤️ using Django + React + PyQt5
