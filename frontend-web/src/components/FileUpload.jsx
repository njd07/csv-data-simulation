import { useState, useCallback } from 'react';
import { dataAPI } from '../api';

function FileUpload({ onUploadSuccess }) {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [dragActive, setDragActive] = useState(false);

    const handleDrag = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    }, []);

    const handleDrop = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const droppedFile = e.dataTransfer.files[0];
            if (droppedFile.name.endsWith('.csv')) {
                setFile(droppedFile);
                setError('');
            } else {
                setError('Please upload a CSV file');
            }
        }
    }, []);

    const handleChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0];
            if (selectedFile.name.endsWith('.csv')) {
                setFile(selectedFile);
                setError('');
            } else {
                setError('Please upload a CSV file');
            }
        }
    };

    const handleUpload = async () => {
        if (!file) {
            setError('Please select a file first');
            return;
        }

        setUploading(true);
        setError('');
        setSuccess('');

        try {
            const response = await dataAPI.upload(file);
            setSuccess(`Successfully uploaded ${response.data.equipment_count} equipment records`);
            setFile(null);
            if (onUploadSuccess) {
                onUploadSuccess(response.data);
            }
        } catch (err) {
            setError(err.response?.data?.error || 'Upload failed');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="upload-section">
            <h2>📤 Upload CSV Data</h2>

            <div
                className={`drop-zone ${dragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                <input
                    type="file"
                    id="file-input"
                    accept=".csv"
                    onChange={handleChange}
                    className="file-input"
                />

                <div className="drop-content">
                    {file ? (
                        <>
                            <div className="file-icon">📄</div>
                            <p className="file-name">{file.name}</p>
                            <p className="file-size">{(file.size / 1024).toFixed(2)} KB</p>
                        </>
                    ) : (
                        <>
                            <div className="upload-icon">📁</div>
                            <p>Drag & drop your CSV file here</p>
                            <span className="or">or</span>
                            <label htmlFor="file-input" className="browse-btn">Browse Files</label>
                        </>
                    )}
                </div>
            </div>

            {file && (
                <button
                    className="upload-btn"
                    onClick={handleUpload}
                    disabled={uploading}
                >
                    {uploading ? (
                        <>
                            <span className="spinner"></span>
                            Uploading...
                        </>
                    ) : (
                        <>🚀 Upload File</>
                    )}
                </button>
            )}

            {error && <div className="error-message">{error}</div>}
            {success && <div className="success-message">{success}</div>}
        </div>
    );
}

export default FileUpload;
