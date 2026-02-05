function History({ history, onSelect, selectedId }) {
    if (!history || history.length === 0) {
        return (
            <div className="history-section">
                <h2>📚 Upload History</h2>
                <div className="empty-state">
                    <div className="empty-icon">📂</div>
                    <p>No upload history</p>
                    <span>Your recent uploads will appear here</span>
                </div>
            </div>
        );
    }

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <div className="history-section">
            <h2>📚 Upload History</h2>
            <p className="history-subtitle">Last 5 uploads (click to view)</p>

            <div className="history-list">
                {history.map((upload) => (
                    <div
                        key={upload.id}
                        className={`history-item ${selectedId === upload.id ? 'selected' : ''}`}
                        onClick={() => onSelect(upload.id)}
                    >
                        <div className="history-icon">📄</div>
                        <div className="history-info">
                            <span className="history-filename">{upload.filename}</span>
                            <span className="history-date">{formatDate(upload.uploaded_at)}</span>
                        </div>
                        <div className="history-count">
                            <span className="count-value">{upload.record_count}</span>
                            <span className="count-label">records</span>
                        </div>
                        {selectedId === upload.id && (
                            <div className="selected-badge">✓</div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default History;
