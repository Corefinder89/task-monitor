from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Enable CORS for all domains

class DataProcessor:
    def __init__(self):
        self.databag_path = os.path.join(os.path.dirname(__file__), '..', 'databag')
        
    def load_performance_monitoring_data(self):
        """Load and process performance monitoring data"""
        try:
            file_path = os.path.join(self.databag_path, 'performance-monitoring.csv')
            df = pd.read_csv(file_path)
            
            # Group by process name and calculate averages
            process_data = df.groupby('Name').agg({
                'Memory (MB)': 'mean',
                'CPU (%)': 'mean',
                'PID': 'count'  # Count of occurrences
            }).reset_index()
            
            # Rename columns for clarity
            process_data.columns = ['name', 'avg_memory', 'avg_cpu', 'count']
            
            # Sort by memory usage and take top 15 for better visualization
            process_data = process_data.sort_values('avg_memory', ascending=False).head(15)
            
            return process_data.to_dict('records')
        except Exception as e:
            print(f"Error loading performance monitoring data: {e}")
            return []
    
    def load_performance_snapshot_data(self):
        """Load and process performance snapshot data"""
        try:
            file_path = os.path.join(self.databag_path, 'performance-snapshot.csv')
            df = pd.read_csv(file_path)
            
            # Group by process name and calculate averages
            process_data = df.groupby('Name').agg({
                'Memory (MB)': 'mean',
                'PID': 'count'
            }).reset_index()
            
            # Rename columns for clarity
            process_data.columns = ['name', 'avg_memory', 'count']
            
            # Sort by memory usage and take top 15
            process_data = process_data.sort_values('avg_memory', ascending=False).head(15)
            
            return process_data.to_dict('records')
        except Exception as e:
            print(f"Error loading performance snapshot data: {e}")
            return []
    
    def get_memory_usage_chart_data(self, data_type='monitoring'):
        """Prepare data for nightingale chart showing memory usage"""
        if data_type == 'monitoring':
            data = self.load_performance_monitoring_data()
        else:
            data = self.load_performance_snapshot_data()
        
        chart_data = []
        for item in data:
            chart_data.append({
                'name': item['name'],
                'value': round(item['avg_memory'], 2)
            })
        
        return chart_data
    
    def get_cpu_usage_chart_data(self):
        """Prepare data for nightingale chart showing CPU usage (monitoring data only)"""
        data = self.load_performance_monitoring_data()
        
        chart_data = []
        for item in data:
            if item['avg_cpu'] > 0:  # Only include processes with CPU usage
                chart_data.append({
                    'name': item['name'],
                    'value': round(item['avg_cpu'], 2)
                })
        
        # Sort by CPU usage
        chart_data = sorted(chart_data, key=lambda x: x['value'], reverse=True)
        
        return chart_data

data_processor = DataProcessor()

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('dashboard.html')

@app.route('/test-charts')
def test_charts():
    """Serve the test charts page for debugging"""
    return render_template('test-charts.html')

@app.route('/api/memory-monitoring')
def get_memory_monitoring():
    """API endpoint for memory usage from monitoring data"""
    try:
        data = data_processor.get_memory_usage_chart_data('monitoring')
        return jsonify({
            'success': True,
            'data': data,
            'title': 'Memory Usage (Performance Monitoring)',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/memory-snapshot')
def get_memory_snapshot():
    """API endpoint for memory usage from snapshot data"""
    try:
        data = data_processor.get_memory_usage_chart_data('snapshot')
        return jsonify({
            'success': True,
            'data': data,
            'title': 'Memory Usage (Performance Snapshot)',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cpu-usage')
def get_cpu_usage():
    """API endpoint for CPU usage data"""
    try:
        data = data_processor.get_cpu_usage_chart_data()
        return jsonify({
            'success': True,
            'data': data,
            'title': 'CPU Usage (Performance Monitoring)',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/process-summary')
def get_process_summary():
    """API endpoint for process summary statistics"""
    try:
        monitoring_data = data_processor.load_performance_monitoring_data()
        snapshot_data = data_processor.load_performance_snapshot_data()
        
        summary = {
            'monitoring': {
                'total_processes': len(monitoring_data),
                'total_memory': sum(item['avg_memory'] for item in monitoring_data),
                'total_cpu': sum(item['avg_cpu'] for item in monitoring_data),
                'top_memory_process': max(monitoring_data, key=lambda x: x['avg_memory']) if monitoring_data else None
            },
            'snapshot': {
                'total_processes': len(snapshot_data),
                'total_memory': sum(item['avg_memory'] for item in snapshot_data),
                'top_memory_process': max(snapshot_data, key=lambda x: x['avg_memory']) if snapshot_data else None
            }
        }
        
        return jsonify({
            'success': True,
            'data': summary,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)