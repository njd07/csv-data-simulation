import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title } from 'chart.js';
import { Pie, Bar, Line } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title);

const COLORS = [
    'rgba(99, 102, 241, 0.8)',
    'rgba(16, 185, 129, 0.8)',
    'rgba(245, 158, 11, 0.8)',
    'rgba(239, 68, 68, 0.8)',
    'rgba(139, 92, 246, 0.8)',
    'rgba(6, 182, 212, 0.8)',
];

const BORDER_COLORS = [
    'rgba(99, 102, 241, 1)',
    'rgba(16, 185, 129, 1)',
    'rgba(245, 158, 11, 1)',
    'rgba(239, 68, 68, 1)',
    'rgba(139, 92, 246, 1)',
    'rgba(6, 182, 212, 1)',
];

function Charts({ data, summary }) {
    if (!data || data.length === 0 || !summary) {
        return (
            <div className="charts-section">
                <h2>📈 Visualizations</h2>
                <div className="empty-state">
                    <div className="empty-icon">📉</div>
                    <p>No data available for visualization</p>
                    <span>Upload a CSV file to see charts</span>
                </div>
            </div>
        );
    }

    // Pie Chart - Type Distribution
    const typeLabels = Object.keys(summary.type_distribution || {});
    const typeValues = Object.values(summary.type_distribution || {});

    const pieData = {
        labels: typeLabels,
        datasets: [{
            data: typeValues,
            backgroundColor: COLORS.slice(0, typeLabels.length),
            borderColor: BORDER_COLORS.slice(0, typeLabels.length),
            borderWidth: 2,
        }]
    };

    const pieOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
                labels: {
                    color: '#e2e8f0',
                    font: { size: 12 }
                }
            },
            title: {
                display: true,
                text: 'Equipment Type Distribution',
                color: '#e2e8f0',
                font: { size: 16 }
            }
        }
    };

    // Bar Chart - Flowrate by Equipment
    const sortedByFlowrate = [...data].sort((a, b) => b.flowrate - a.flowrate).slice(0, 10);

    const barData = {
        labels: sortedByFlowrate.map(d => d.name),
        datasets: [{
            label: 'Flowrate',
            data: sortedByFlowrate.map(d => d.flowrate),
            backgroundColor: 'rgba(99, 102, 241, 0.7)',
            borderColor: 'rgba(99, 102, 241, 1)',
            borderWidth: 2,
            borderRadius: 8,
        }]
    };

    const barOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            title: {
                display: true,
                text: 'Top 10 Equipment by Flowrate',
                color: '#e2e8f0',
                font: { size: 16 }
            }
        },
        scales: {
            x: {
                ticks: { color: '#a0aec0' },
                grid: { color: 'rgba(255,255,255,0.1)' }
            },
            y: {
                ticks: { color: '#a0aec0' },
                grid: { color: 'rgba(255,255,255,0.1)' }
            }
        }
    };

    // Line Chart - Pressure vs Temperature
    const lineData = {
        labels: data.map(d => d.name),
        datasets: [
            {
                label: 'Pressure (bar)',
                data: data.map(d => d.pressure),
                borderColor: 'rgba(16, 185, 129, 1)',
                backgroundColor: 'rgba(16, 185, 129, 0.2)',
                tension: 0.4,
                fill: true,
            },
            {
                label: 'Temperature (°C)',
                data: data.map(d => d.temperature),
                borderColor: 'rgba(239, 68, 68, 1)',
                backgroundColor: 'rgba(239, 68, 68, 0.2)',
                tension: 0.4,
                fill: true,
            }
        ]
    };

    const lineOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: { color: '#e2e8f0' }
            },
            title: {
                display: true,
                text: 'Pressure vs Temperature Comparison',
                color: '#e2e8f0',
                font: { size: 16 }
            }
        },
        scales: {
            x: {
                ticks: { color: '#a0aec0', maxRotation: 45 },
                grid: { color: 'rgba(255,255,255,0.1)' }
            },
            y: {
                ticks: { color: '#a0aec0' },
                grid: { color: 'rgba(255,255,255,0.1)' }
            }
        }
    };

    return (
        <div className="charts-section">
            <h2>📈 Visualizations</h2>

            <div className="charts-grid">
                <div className="chart-card">
                    <div className="chart-container pie-chart">
                        <Pie data={pieData} options={pieOptions} />
                    </div>
                </div>

                <div className="chart-card">
                    <div className="chart-container bar-chart">
                        <Bar data={barData} options={barOptions} />
                    </div>
                </div>

                <div className="chart-card full-width">
                    <div className="chart-container line-chart">
                        <Line data={lineData} options={lineOptions} />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Charts;
