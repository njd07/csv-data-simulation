function Summary({ summary }) {
    if (!summary || summary.total_count === 0) {
        return (
            <div className="summary-section">
                <h2>📋 Summary Statistics</h2>
                <div className="empty-state">
                    <div className="empty-icon">📊</div>
                    <p>No summary available</p>
                    <span>Upload data to see statistics</span>
                </div>
            </div>
        );
    }

    const stats = [
        {
            label: 'Total Equipment',
            value: summary.total_count,
            icon: '🔧',
            color: 'blue'
        },
        {
            label: 'Avg Flowrate',
            value: summary.avg_flowrate?.toFixed(2) || '0',
            icon: '💧',
            color: 'cyan'
        },
        {
            label: 'Avg Pressure',
            value: `${summary.avg_pressure?.toFixed(2) || '0'} bar`,
            icon: '⚡',
            color: 'green'
        },
        {
            label: 'Avg Temperature',
            value: `${summary.avg_temperature?.toFixed(1) || '0'}°C`,
            icon: '🌡️',
            color: 'orange'
        }
    ];

    const ranges = [
        {
            label: 'Flowrate Range',
            min: summary.min_flowrate?.toFixed(1),
            max: summary.max_flowrate?.toFixed(1),
            icon: '💧'
        },
        {
            label: 'Pressure Range',
            min: `${summary.min_pressure?.toFixed(2)} bar`,
            max: `${summary.max_pressure?.toFixed(2)} bar`,
            icon: '⚡'
        },
        {
            label: 'Temperature Range',
            min: `${summary.min_temperature?.toFixed(1)}°C`,
            max: `${summary.max_temperature?.toFixed(1)}°C`,
            icon: '🌡️'
        }
    ];

    return (
        <div className="summary-section">
            <h2>📋 Summary Statistics</h2>

            <div className="stats-grid">
                {stats.map((stat, index) => (
                    <div key={index} className={`stat-card stat-${stat.color}`}>
                        <div className="stat-icon">{stat.icon}</div>
                        <div className="stat-info">
                            <span className="stat-label">{stat.label}</span>
                            <span className="stat-value">{stat.value}</span>
                        </div>
                    </div>
                ))}
            </div>

            <div className="ranges-section">
                <h3>📏 Value Ranges</h3>
                <div className="ranges-grid">
                    {ranges.map((range, index) => (
                        <div key={index} className="range-card">
                            <span className="range-icon">{range.icon}</span>
                            <div className="range-info">
                                <span className="range-label">{range.label}</span>
                                <div className="range-values">
                                    <span className="min-value">Min: {range.min}</span>
                                    <span className="range-arrow">→</span>
                                    <span className="max-value">Max: {range.max}</span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {summary.type_distribution && Object.keys(summary.type_distribution).length > 0 && (
                <div className="distribution-section">
                    <h3>🏭 Equipment Types</h3>
                    <div className="type-badges">
                        {Object.entries(summary.type_distribution).map(([type, count]) => (
                            <div key={type} className="type-item">
                                <span className={`type-badge type-${type.toLowerCase()}`}>{type}</span>
                                <span className="type-count">{count}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default Summary;
