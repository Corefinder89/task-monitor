# Task Monitor Application

A Python-based system performance monitoring tool that captures running processes and saves performance data to CSV files. The application supports both single-snapshot and continuous monitoring modes.

## Features

- 🖥️ **Process Monitoring** - Tracks top memory-consuming processes with CPU usage
- 📊 **Dual Modes** - Single snapshot or continuous monitoring
- 🗂️ **CSV Export** - Saves performance data with timestamps
- 📝 **Centralized Logging** - Structured logging with detailed process information
- ⚙️ **Configurable** - Customizable process limits and monitoring intervals
- 🔇 **Silent Operation** - Monitoring runs without screen output for background use

## Project Structure

```
task-monitor/
├── app/
│   ├── requirements.txt     # Python dependencies
│   └── src/
│       ├── csvconverter.py   # CSV generation and monitoring orchestration
│       ├── gettasks.py      # Process data collection and monitoring
│       └── utils/
│           ├── logger_utils.py    # Centralized logging system
│           ├── logging_config.py  # Logging configuration
│           └── __init__.py
├── logs/                    # Application log files (auto-created)
├── run.py                   # Main application entry point
└── start.sh                 # Bash startup script
```

## Generated Files
- `performance-snapshot.csv` - Single snapshot data
- `performance-monitoring.csv` - Continuous monitoring data

## Quick Start

### Option 1: Using Python directly (Recommended)
```bash
# Take a single performance snapshot
python3 run.py --snapshot

# Start continuous monitoring
python3 run.py --monitor

# Custom options
python3 run.py --snapshot --limit 10
python3 run.py --monitor --limit 15 --interval 5
```

### Option 2: Using the startup script
```bash
# Note: You may need to modify start.sh for new command structure
./start.sh
```

## 📊 Web Dashboard (NEW!)

We now include a beautiful web-based dashboard using **Apache ECharts** to visualize your performance data with interactive nightingale (rose) charts!

### Features
- 🌹 **Nightingale Charts** - Beautiful rose/radial charts for memory and CPU data
- 📱 **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- 🔄 **Real-time Updates** - Auto-refresh every 30 seconds or manual refresh
- 📈 **Multiple Views** - Separate charts for monitoring and snapshot data
- 🎨 **Modern UI** - Clean gradient design with smooth animations

### Quick Dashboard Setup
```bash
# Option 1: Use the convenient startup script
./start_dashboard.sh

# Option 2: Manual setup
cd app
pip install -r requirements.txt
python backend_server.py
```

Then open your browser and navigate to: **http://localhost:5000**

### Dashboard Requirements
- Existing CSV files in `databag/` directory (generated from monitoring)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Python Flask dependencies (automatically installed)

> 💡 **Tip**: First run some monitoring to generate CSV data, then launch the dashboard to see your beautiful charts!

For detailed dashboard setup and customization instructions, see [ECHARTS_README.md](ECHARTS_README.md)

## Command Line Options

```bash
python3 run.py {--snapshot|--monitor} [OPTIONS]

Required (choose one):
  --snapshot            Take a single performance snapshot and exit
  --monitor             Start continuous monitoring mode (stop with Ctrl+C)

Optional arguments:
  -h, --help           Show help message
  --limit LIMIT        Number of top processes to monitor (default: 20)
  --interval INTERVAL  Monitoring refresh interval in seconds (default: 2, only for --monitor)
```
```

## Usage Examples

### Snapshot Mode
```bash
# Quick snapshot with default settings (top 20 processes)
python3 run.py --snapshot

# Snapshot with fewer processes
python3 run.py --snapshot --limit 10

# Snapshot with more processes  
python3 run.py --snapshot --limit 50
```

### Monitoring Mode
```bash
# Start continuous monitoring (default: top 20 processes, 2-second interval)
python3 run.py --monitor

# Custom monitoring settings
python3 run.py --monitor --limit 15 --interval 5

# Light monitoring (fewer processes, longer interval for low resource usage)
python3 run.py --monitor --limit 5 --interval 10
```

> **Note**: Monitoring mode runs silently and logs detailed process information. Stop with Ctrl+C.

## Output

The application generates:

### CSV Files
- **Snapshot Mode**: `performance-snapshot.csv`
  - Single timestamp with top memory processes
  - Columns: Timestamp, PID, Name, Memory (MB)

- **Monitoring Mode**: `performance-monitoring.csv` 
  - Continuous data collection with timestamps
  - Columns: Timestamp, PID, Name, Memory (MB), CPU %
  - Data appended every monitoring interval

### Logging Output
- **Console Logging**: Real-time status messages and process details
- **File Logging**: Structured logs in `logs/task-monitor.log` (auto-created)
- **Process Details**: Individual process polling information (PID, name, memory, CPU)

## Sample Output

### Console Output - Snapshot Mode
```
INFO - 📊 Taking performance snapshot...
INFO - Collected 156 processes, 23 access errors, returning top 20
INFO - Data successfully written to performance-snapshot.csv
INFO - ✅ Snapshot saved to performance-snapshot.csv
```

### Console Output - Monitoring Mode
```
INFO - 🔄 Starting continuous monitoring mode...
INFO - 📊 Monitoring top 20 processes every 2 seconds
INFO - Polled process: Chrome (PID: 1234) - Memory: 512.45 MB, CPU: 3.2%
INFO - Polled process: VSCode (PID: 5678) - Memory: 387.21 MB, CPU: 1.8%
INFO - Polled process: Python (PID: 9012) - Memory: 156.78 MB, CPU: 0.5%
...
INFO - ✅ Monitoring completed
```

### CSV Output - Snapshot
```csv
Timestamp,PID,Name,Memory (MB)
2026-02-07 13:45:23,1234,Chrome,512.45
2026-02-07 13:45:23,5678,VSCode,387.21
2026-02-07 13:45:23,9012,Python,156.78
```

### CSV Output - Monitoring  
```csv
Timestamp,PID,Name,Memory (MB),CPU %
2026-02-07 13:45:23,1234,Chrome,512.45,3.2
2026-02-07 13:45:25,1234,Chrome,514.12,2.8
2026-02-07 13:45:27,1234,Chrome,515.67,4.1
```

## Requirements

- Python 3.7+
- psutil package

### Installation
```bash
# Install dependencies
pip install -r app/requirements.txt

# Or install psutil directly
pip install psutil
```

## Development

### Project Architecture
- **`run.py`**: Main entry point with command-line interface
- **`app/src/csvconverter.py`**: CSV generation and monitoring orchestration
- **`app/src/gettasks.py`**: Process data collection with detailed logging
- **`app/src/utils/`**: Centralized logging utilities

### Adding New Features
1. Add new modules in `app/src/`
2. Use the centralized logger: `from app.src.utils.logger_utils import get_logger`
3. Update the main application in `run.py`

### Logging System
The application uses a centralized logging system that provides:
- **Console output**: Real-time status and process information  
- **File logging**: Structured logs with timestamps in `logs/`
- **Process monitoring**: Detailed logging of each polled process (name, PID, memory, CPU)
- **Error tracking**: Debug-level logging for process access errors

Modify `app/src/utils/logging_config.py` to customize:
- Log levels and formatting
- Output destinations (console, file, both)

## Troubleshooting

### Common Issues

1. **Permission Errors**: Some processes may not be accessible
   - This is normal and logged at debug level
   - The application continues with accessible processes
   - Use higher `--limit` values to ensure you get enough data

2. **Python Path Issues**: 
   - Always use `python3 run.py` from the project root directory
   - The script handles Python path configuration automatically

3. **Missing Dependencies**:
   ```bash
   cd task-monitor
   pip install -r app/requirements.txt
   ```

4. **Mode Selection**: 
   - You must choose either `--snapshot` or `--monitor`
   - Both modes cannot be used simultaneously
   
5. **Monitoring Not Stopping**:
   - Use Ctrl+C to gracefully stop monitoring mode
   - Data will be saved before exit

### Debug Information
The application provides detailed logging. For troubleshooting:

1. **Check process access**: Some processes may be restricted
   ```bash
   # Run with more processes to account for access denials
   python3 run.py --snapshot --limit 50
   ```

2. **Verify CSV output**: Check generated files in project directory
   - `performance-snapshot.csv` for snapshot mode
   - `performance-monitoring.csv` for monitoring mode

3. **Review logs**: Check `logs/task-monitor.log` for detailed information

## License

This project is open source. Feel free to modify and distribute.