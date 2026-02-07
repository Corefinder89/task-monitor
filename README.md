# Task Monitor Application

A Python-based system performance monitoring tool that captures running processes and saves performance data to CSV files.

## Features

- 🖥️ **Process Monitoring** - Tracks top memory-consuming processes
- 📊 **CSV Export** - Saves performance data with timestamps
- 📝 **Centralized Logging** - Structured logging across all modules
- ⚙️ **Configurable** - Customizable process limits and output formats
- 🚀 **Easy to Use** - Simple command-line interface

## Project Structure

```
task-monitor/
├── app/
│   ├── main.py              # Main application entry point
│   ├── requirements.txt     # Python dependencies
│   └── src/
│       ├── convertcsv.py    # CSV conversion functionality
│       ├── gettasks.py      # Process monitoring
│       ├── utils/
│       │   ├── logger_utils.py  # Centralized logging system
│       │   └── logging_config.py # Logging configuration
├── logs/                    # Application log files (auto-created)
├── run.py                   # Simple runner script
├── start.sh                 # Bash startup script
└── performance-monitor.csv  # Generated CSV output (after running)
```

## Quick Start

### Option 1: Using the startup script (Recommended)
```bash
# Make sure the script is executable (already done)
./start.sh

# Or with options
./start.sh --processes 15 --log-level DEBUG
```

### Option 2: Using Python directly
```bash
# Run with default settings
python3 run.py

# Or run the main application directly
python3 app/main.py

# With custom options
python3 app/main.py --processes 25 --log-level INFO --output my-performance.csv
```

## Command Line Options

```bash
python3 app/main.py [OPTIONS]

Options:
  -h, --help            Show help message
  -l, --log-level       Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  -f, --log-file        Specify log file path
  -p, --processes       Number of top processes to monitor (default: 20)
  -o, --output          Output CSV file name (default: performance-monitor.csv)
  --version            Show version information
```

## Usage Examples

### Basic Usage
```bash
# Monitor top 20 processes (default)
python3 run.py
```

### Advanced Usage
```bash
# Monitor top 10 processes with debug logging
python3 app/main.py --processes 10 --log-level DEBUG

# Save to custom file with log file
python3 app/main.py --output "system-report.csv" --log-file "logs/debug.log"

# Silent operation (errors only)
python3 app/main.py --log-level ERROR
```

## Output

The application generates:

1. **CSV File**: `performance-monitor.csv` (or custom name)
   - Columns: Timestamp, PID, Name, Memory (MB)
   - Sorted by memory usage (highest first)

2. **Log Files**: In the `logs/` directory
   - Console output with timestamps
   - Optional file logging

## Sample Output

### Console Output
```
2026-02-07 13:45:23 - __main__ - INFO - ============================================================
2026-02-07 13:45:23 - __main__ - INFO - 🖥️  TASK MONITOR APPLICATION STARTING
2026-02-07 13:45:23 - __main__ - INFO - ============================================================
2026-02-07 13:45:23 - __main__ - INFO - 📊 Collecting system process data...
2026-02-07 13:45:23 - process_monitor - INFO - Collected 156 processes, 23 access errors, returning top 20
2026-02-07 13:45:23 - __main__ - INFO - ✅ Collected 20 processes
2026-02-07 13:45:23 - __main__ - INFO - 💾 Total memory usage: 2847.32 MB
2026-02-07 13:45:23 - __main__ - INFO - 💾 Saving performance data to CSV...
2026-02-07 13:45:23 - csv_converter - INFO - Data successfully written to performance-monitor.csv
2026-02-07 13:45:23 - __main__ - INFO - 🎉 Application completed successfully!
```

### CSV Output
```csv
Timestamp,PID,Name,Memory (MB)
2026-02-07 13:45:23,1234,Chrome,512.45
2026-02-07 13:45:23,5678,VSCode,387.21
2026-02-07 13:45:23,9012,Python,156.78
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

### Adding New Features
1. Add new modules in `app/src/`
2. Use the centralized logger: `from app.src.utils import get_logger`
3. Update the main application in `app/main.py`

### Logging Configuration
Modify `app/src/utils/logging_config.py` to customize:
- Log levels
- Output destinations (console, file, both)
- Log formatting

## Troubleshooting

### Common Issues

1. **Permission Errors**: Some processes may not be accessible
   - This is normal and logged as debug messages
   - The application continues with accessible processes

2. **Python Path Issues**: 
   - Use the provided `run.py` or `start.sh` scripts
   - They handle path configuration automatically

3. **Missing Dependencies**:
   ```bash
   pip install psutil
   ```

### Debug Mode
```bash
python3 app/main.py --log-level DEBUG
```

## License

This project is open source. Feel free to modify and distribute.