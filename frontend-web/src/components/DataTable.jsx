import { useState } from 'react';

function DataTable({ data }) {
    const [currentPage, setCurrentPage] = useState(1);
    const [sortField, setSortField] = useState('name');
    const [sortDirection, setSortDirection] = useState('asc');
    const [searchTerm, setSearchTerm] = useState('');
    const itemsPerPage = 10;

    if (!data || data.length === 0) {
        return (
            <div className="table-section">
                <h2>📊 Equipment Data</h2>
                <div className="empty-state">
                    <div className="empty-icon">📭</div>
                    <p>No equipment data available</p>
                    <span>Upload a CSV file to see data here</span>
                </div>
            </div>
        );
    }

    // Filter data
    const filteredData = data.filter(item =>
        item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.type.toLowerCase().includes(searchTerm.toLowerCase())
    );

    // Sort data
    const sortedData = [...filteredData].sort((a, b) => {
        let aVal = a[sortField];
        let bVal = b[sortField];

        if (typeof aVal === 'string') {
            aVal = aVal.toLowerCase();
            bVal = bVal.toLowerCase();
        }

        if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
        if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
        return 0;
    });

    // Paginate
    const totalPages = Math.ceil(sortedData.length / itemsPerPage);
    const startIndex = (currentPage - 1) * itemsPerPage;
    const paginatedData = sortedData.slice(startIndex, startIndex + itemsPerPage);

    const handleSort = (field) => {
        if (sortField === field) {
            setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
        } else {
            setSortField(field);
            setSortDirection('asc');
        }
    };

    const renderSortIcon = (field) => {
        if (sortField !== field) return '↕️';
        return sortDirection === 'asc' ? '⬆️' : '⬇️';
    };

    return (
        <div className="table-section">
            <div className="table-header">
                <h2>📊 Equipment Data</h2>
                <div className="search-box">
                    <input
                        type="text"
                        placeholder="Search equipment..."
                        value={searchTerm}
                        onChange={(e) => {
                            setSearchTerm(e.target.value);
                            setCurrentPage(1);
                        }}
                    />
                    <span className="search-icon">🔍</span>
                </div>
            </div>

            <div className="table-wrapper">
                <table className="data-table">
                    <thead>
                        <tr>
                            <th onClick={() => handleSort('name')}>
                                Name {renderSortIcon('name')}
                            </th>
                            <th onClick={() => handleSort('type')}>
                                Type {renderSortIcon('type')}
                            </th>
                            <th onClick={() => handleSort('flowrate')}>
                                Flowrate {renderSortIcon('flowrate')}
                            </th>
                            <th onClick={() => handleSort('pressure')}>
                                Pressure (bar) {renderSortIcon('pressure')}
                            </th>
                            <th onClick={() => handleSort('temperature')}>
                                Temp (°C) {renderSortIcon('temperature')}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {paginatedData.map((item, index) => (
                            <tr key={item.id || index}>
                                <td className="name-cell">{item.name}</td>
                                <td>
                                    <span className={`type-badge type-${item.type.toLowerCase()}`}>
                                        {item.type}
                                    </span>
                                </td>
                                <td>{item.flowrate.toFixed(1)}</td>
                                <td>{item.pressure.toFixed(2)}</td>
                                <td>{item.temperature.toFixed(1)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="pagination">
                <span className="page-info">
                    Showing {startIndex + 1}-{Math.min(startIndex + itemsPerPage, sortedData.length)} of {sortedData.length}
                </span>
                <div className="page-controls">
                    <button
                        onClick={() => setCurrentPage(1)}
                        disabled={currentPage === 1}
                    >
                        ⏮️
                    </button>
                    <button
                        onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                        disabled={currentPage === 1}
                    >
                        ◀️
                    </button>
                    <span className="page-number">{currentPage} / {totalPages}</span>
                    <button
                        onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                        disabled={currentPage === totalPages}
                    >
                        ▶️
                    </button>
                    <button
                        onClick={() => setCurrentPage(totalPages)}
                        disabled={currentPage === totalPages}
                    >
                        ⏭️
                    </button>
                </div>
            </div>
        </div>
    );
}

export default DataTable;
