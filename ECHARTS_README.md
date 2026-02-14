# Task Monitor Dashboard with Apache ECharts

A comprehensive web-based dashboard for visualizing system process performance data using Apache ECharts nightingale (rose) charts. This application combines a Python Flask backend with a modern frontend to present process monitoring data in an elegant, interactive format.

## Features

- 🌹 **Nightingale Charts**: Beautiful rose/radial charts for data visualization
- 📊 **Multiple Data Views**: Memory and CPU usage from both monitoring and snapshot data
- 🔄 **Real-time Updates**: Auto-refresh capabilities with manual refresh options
- 📱 **Responsive Design**: Mobile-friendly interface that works on all devices
- 🎨 **Modern UI**: Clean, gradient-based design with smooth animations
- 📈 **Statistical Summary**: Overview cards showing key metrics
- 🔍 **Interactive Charts**: Hover effects and detailed tooltips

## Architecture

```
├── Backend (Python Flask)
│   ├── Data processing from CSV files
│   ├── RESTful API endpoints
│   └── Statistical calculations
└── Frontend (HTML/CSS/JavaScript)
    ├── Apache ECharts integration
    ├── Responsive dashboard layout
    └── Auto-refresh functionality
```

## Prerequisites

- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- CSV data files in the `databag/` directory

## Installation & Setup

### 1. Clone and Navigate to Project
```bash
cd /path/to/your/task-monitor
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
cd app
pip install -r requirements.txt
```

### 4. Verify Data Files
Ensure you have the following CSV files in the `databag/` directory:
- `performance-monitoring.csv` - Contains: Timestamp, PID, Name, Memory (MB), CPU (%)
- `performance-snapshot.csv` - Contains: Timestamp, PID, Name, Memory (MB)

### 5. Run the Application
```bash
python backend_server.py
```

The server will start on `http://localhost:5000`

### 6. Access the Dashboard
Open your web browser and navigate to:
```
http://localhost:5000
```

## CSV Data Format

### performance-monitoring.csv
```csv
Timestamp,PID,Name,Memory (MB),CPU (%)
2026-02-14 17:31:38,8456,node,527.1,1.0
2026-02-14 17:31:38,8230,node,139.68,0.0
...
```

### performance-snapshot.csv
```csv
Timestamp,PID,Name,Memory (MB)
2026-02-14 17:31:21,8456,node,526.60
2026-02-14 17:31:21,8230,node,139.68
...
```

## API Endpoints

The backend provides the following REST API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard page |
| `/api/memory-monitoring` | GET | Memory usage from monitoring data |
| `/api/memory-snapshot` | GET | Memory usage from snapshot data |
| `/api/cpu-usage` | GET | CPU usage distribution |
| `/api/process-summary` | GET | Statistical summary of all data |

### Example API Response
```json
{
    "success": true,
    "data": [
        {"name": "node", "value": 527.1},
        {"name": "python3.10", "value": 105.64},
        {"name": "snapd", "value": 38.21}
    ],
    "title": "Memory Usage (Performance Monitoring)",
    "timestamp": "2026-02-14T17:31:38"
}
```

## Apache ECharts Configuration

The dashboard uses Apache ECharts 5.4.3 with the following chart configurations:

### Nightingale (Rose) Chart Features:
- **Chart Type**: `pie` with `roseType: 'area'`
- **Visual Style**: Gradient colors with border radius
- **Interactive Elements**: Hover effects and shadows
- **Data Labels**: Process names and values
- **Legend**: Vertical layout with name truncation
- **Tooltips**: Detailed information with percentages

### Chart Customization Options:
```javascript
// Example configuration
{
    radius: ['20%', '70%'],     // Inner and outer radius
    roseType: 'area',           // Rose chart type
    itemStyle: {
        borderRadius: 8,        // Rounded corners
        borderColor: '#fff',    // White border
        borderWidth: 2
    }
}
```

## Dashboard Features

### 1. Statistical Overview
- Total number of processes
- Total memory consumption
- Total CPU usage
- Last update timestamp

### 2. Interactive Charts
- **Memory Usage (Monitoring)**: Shows average memory usage per process
- **Memory Usage (Snapshot)**: Displays snapshot memory data
- **CPU Usage Distribution**: Visualizes CPU usage patterns

### 3. Control Features
- **Refresh All Charts**: Manual refresh button
- **Individual Chart Refresh**: Per-chart refresh buttons
- **Auto-refresh Toggle**: Automatic updates every 30 seconds
- **Responsive Design**: Adapts to different screen sizes

## Customization

### Modifying Chart Colors
Edit the colors array in `/app/static/js/dashboard.js`:
```javascript
const colors = [
    '#ff6b6b', '#4ecdc4', '#45b7d1', // Add your colors here
    // ... more colors
];
```

### Changing Refresh Interval
Modify the interval in the JavaScript file:
```javascript
this.refreshIntervalTime = 30000; // 30 seconds (in milliseconds)
```

### Adding New Chart Types
1. Add new API endpoint in `backend_server.py`
2. Create chart container in `dashboard.html`
3. Implement chart logic in `dashboard.js`

## Troubleshooting

### Common Issues

**1. Charts not loading**
- Check browser console for JavaScript errors
- Verify API endpoints are returning data
- Ensure CSV files exist and have correct format

**2. Flask server not starting**
- Verify all dependencies are installed: `pip list`
- Check for port conflicts (try different port: `app.run(port=5001)`)
- Ensure proper working directory

**3. Data not displaying**
- Verify CSV file format matches expected structure
- Check file permissions for databag directory
- Review browser network tab for API call failures

**4. Responsive issues**
- Clear browser cache
- Check CSS media queries
- Verify viewport meta tag in HTML

### Debug Mode
Enable Flask debug mode for development:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Performance Optimization

### Backend Optimizations
- Data caching for frequently accessed endpoints
- Efficient pandas operations
- Limited data points (top 15 processes) for better visualization

### Frontend Optimizations
- Chart instance reuse
- Automatic cleanup on page unload
- Optimized refresh intervals
- Lazy loading of chart data

## Browser Support

The dashboard supports modern browsers:
- ✅ Chrome 70+
- ✅ Firefox 65+
- ✅ Safari 12+
- ✅ Edge 79+

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Dependencies

### Python Backend
- `flask~=2.3.3` - Web framework
- `flask-cors~=4.0.0` - CORS support
- `pandas~=2.1.0` - Data processing
- `psutil~=7.2.2` - System monitoring

### Frontend
- `Apache ECharts 5.4.3` - Chart library (CDN)
- Modern CSS3 features
- Vanilla JavaScript (ES6+)

## License

This project is part of the task-monitor application. Please refer to the main project license.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review browser console for error messages
3. Verify all setup steps are completed correctly
4. Check API endpoints manually for data availability

---

**Happy Monitoring!** 📊✨