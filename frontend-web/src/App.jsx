import { useState, useEffect } from 'react';
import Login from './components/Login';
import FileUpload from './components/FileUpload';
import DataTable from './components/DataTable';
import Charts from './components/Charts';
import Summary from './components/Summary';
import History from './components/History';
import { dataAPI } from './api';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [data, setData] = useState([]);
  const [summary, setSummary] = useState(null);
  const [history, setHistory] = useState([]);
  const [selectedUploadId, setSelectedUploadId] = useState(null);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    const savedToken = localStorage.getItem('token');
    if (savedUser && savedToken) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  useEffect(() => {
    if (user) {
      fetchData();
      fetchHistory();
    }
  }, [user, selectedUploadId]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [dataRes, summaryRes] = await Promise.all([
        dataAPI.getData(selectedUploadId),
        dataAPI.getSummary(selectedUploadId)
      ]);
      setData(dataRes.data);
      setSummary(summaryRes.data);
    } catch (err) {
      console.error('Failed to fetch data:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchHistory = async () => {
    try {
      const res = await dataAPI.getHistory();
      setHistory(res.data);
    } catch (err) {
      console.error('Failed to fetch history:', err);
    }
  };

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setData([]);
    setSummary(null);
    setHistory([]);
  };

  const handleUploadSuccess = () => {
    setSelectedUploadId(null);
    fetchData();
    fetchHistory();
  };

  const handleSelectUpload = (uploadId) => {
    setSelectedUploadId(uploadId === selectedUploadId ? null : uploadId);
  };

  const handleDownloadPDF = async () => {
    try {
      await dataAPI.downloadReport(selectedUploadId);
    } catch (err) {
      console.error('Failed to download PDF:', err);
    }
  };

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-left">
          <div className="logo">⚗️</div>
          <div className="brand">
            <h1>Chemical Equipment</h1>
            <span>Analysis Platform</span>
          </div>
        </div>

        <nav className="nav-tabs">
          <button
            className={`nav-tab ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            📊 Dashboard
          </button>
          <button
            className={`nav-tab ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => setActiveTab('upload')}
          >
            📤 Upload
          </button>
          <button
            className={`nav-tab ${activeTab === 'data' ? 'active' : ''}`}
            onClick={() => setActiveTab('data')}
          >
            📋 Data
          </button>
          <button
            className={`nav-tab ${activeTab === 'charts' ? 'active' : ''}`}
            onClick={() => setActiveTab('charts')}
          >
            📈 Charts
          </button>
        </nav>

        <div className="header-right">
          <button className="pdf-btn" onClick={handleDownloadPDF} disabled={data.length === 0}>
            📥 PDF Report
          </button>
          <div className="user-info">
            <span className="user-icon">👤</span>
            <span className="username">{user.username}</span>
          </div>
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <main className="app-main">
        {loading && (
          <div className="loading-overlay">
            <div className="loader"></div>
          </div>
        )}

        <aside className="sidebar">
          <History
            history={history}
            onSelect={handleSelectUpload}
            selectedId={selectedUploadId}
          />
        </aside>

        <section className="content">
          {activeTab === 'dashboard' && (
            <>
              <Summary summary={summary} />
              <Charts data={data} summary={summary} />
            </>
          )}

          {activeTab === 'upload' && (
            <FileUpload onUploadSuccess={handleUploadSuccess} />
          )}

          {activeTab === 'data' && (
            <DataTable data={data} />
          )}

          {activeTab === 'charts' && (
            <Charts data={data} summary={summary} />
          )}
        </section>
      </main>

      <footer className="app-footer">
        <p>Chemical Equipment Analysis Platform © 2026 | Built with Django + React</p>
      </footer>
    </div>
  );
}

export default App;
