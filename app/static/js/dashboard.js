// Dashboard JavaScript for D3.js Nightingale Charts
// Note: Global refresh functions are defined inline in HTML for immediate availability

// Dashboard JavaScript for D3.js Nightingale Charts
class TaskMonitorDashboard {
    constructor() {
        this.charts = {};
        this.autoRefreshInterval = null;
        this.isAutoRefreshEnabled = false;
        this.refreshIntervalTime = 30000; // 30 seconds
        
        this.init();
    }
    
    init() {
        console.log('🚀 TaskMonitorDashboard initializing...');
        console.log('D3.js available:', typeof d3 !== 'undefined');
        
        // Initialize all charts
        this.initializeCharts();
        
        // Load initial data
        this.refreshAllCharts();
        
        // Load summary statistics
        this.loadSummaryStats();
        
        // Set up event listeners
        this.setupEventListeners();
        
        console.log('✅ TaskMonitorDashboard initialized successfully');
    }
    
    initializeCharts() {
        console.log('📊 Initializing charts...');
        
        // Check if D3.js is available
        if (typeof d3 === 'undefined') {
            console.error('❌ D3.js library not loaded!');
            return;
        }
        console.log('✅ D3.js library is available');
        
        // Initialize Memory Monitoring Chart (Nightingale/Rose Chart)
        const memoryMonitoringEl = document.getElementById('memory-monitoring-chart');
        if (memoryMonitoringEl) {
            this.charts.memoryMonitoring = { element: memoryMonitoringEl };
            console.log('✅ Memory monitoring chart container ready');
        } else {
            console.error('❌ memory-monitoring-chart element not found');
        }
        
        // Initialize Memory Snapshot Chart (Nightingale/Rose Chart)
        const memorySnapshotEl = document.getElementById('memory-snapshot-chart');
        if (memorySnapshotEl) {
            this.charts.memorySnapshot = { element: memorySnapshotEl };
            console.log('✅ Memory snapshot chart container ready');
        } else {
            console.error('❌ memory-snapshot-chart element not found');
        }
        
        // Initialize CPU Usage Chart (Nightingale/Rose Chart)
        const cpuUsageEl = document.getElementById('cpu-usage-chart');
        if (cpuUsageEl) {
            this.charts.cpuUsage = { element: cpuUsageEl };
            console.log('✅ CPU usage chart container ready');
        } else {
            console.error('❌ cpu-usage-chart element not found');
        }
        
        // Handle window resize
        window.addEventListener('resize', () => {
            this.refreshAllCharts();
        });
        
        console.log('📊 Charts initialization complete');
    }
    
    setupEventListeners() {
        // Event listeners are set up, global functions defined above
        console.log('✅ Event listeners set up');
    }
    
    createNightingaleChart(data, title, containerElement, unit = 'MB') {
        // Clear previous chart
        d3.select(containerElement).selectAll("*").remove();
        
        // Color palette matching ECharts style
        const colorScale = d3.scaleOrdinal([
            '#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de',
            '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc', '#ffb347',
            '#87ceeb', '#32cd32', '#ff6347', '#dda0dd', '#98fb98',
            '#f0e68c', '#ff69b4', '#87cefa', '#daa520', '#98d8c8'
        ]);
        
        // Chart dimensions and margins - improved spacing
        const container = d3.select(containerElement);
        const width = 650;
        const height = 450;
        const margin = { top: 70, right: 50, bottom: 50, left: 50 };
        const innerRadius = 35;
        const outerRadius = Math.min(width - margin.left - margin.right, height - margin.top - margin.bottom) / 2 * 0.65;
        
        // Create SVG
        const svg = container.append("svg")
            .attr("width", width)
            .attr("height", height);
        
        // Title - left aligned to prevent cutting
        svg.append("text")
            .attr("x", margin.left)
            .attr("y", 25)
            .attr("text-anchor", "start")
            .attr("class", "chart-title")
            .style("font-size", "16px")
            .style("font-weight", "bold")
            .style("fill", "#333")
            .text(title.length > 40 ? title.substring(0, 40) + '...' : title);
            
        svg.append("text")
            .attr("x", margin.left)
            .attr("y", 45)
            .attr("text-anchor", "start")
            .attr("class", "chart-subtitle")
            .style("font-size", "12px")
            .style("fill", "#666")
            .text("Process Performance Data");
        
        // Chart group - adjusted positioning
        const g = svg.append("g")
            .attr("transform", `translate(${width / 2 - 90},${height / 2 + 10})`);
        
        // Calculate total for percentages
        const total = d3.sum(data, d => d.value);
        
        // Create pie generator
        const pie = d3.pie()
            .value(d => d.value)
            .sort(null);
        
        // Create arc generator for outer (value-based radius)
        const arc = d3.arc()
            .innerRadius(innerRadius)
            .outerRadius(d => {
                // Scale radius based on value for nightingale/rose effect
                const scale = d3.scaleSqrt()
                    .domain([0, d3.max(data, item => item.value)])
                    .range([innerRadius + 20, outerRadius]);
                return scale(d.data.value);
            });
        
        // Create arc generator for labels
        const labelArc = d3.arc()
            .innerRadius(outerRadius + 10)
            .outerRadius(outerRadius + 10);
        
        // Create arc generator for polylines
        const polylineArc = d3.arc()
            .innerRadius(outerRadius + 5)
            .outerRadius(outerRadius + 5);
        
        // Add pie slices
        const pieSlices = g.selectAll(".arc")
            .data(pie(data))
            .enter().append("g")
            .attr("class", "arc");
        
        // Add paths for slices
        pieSlices.append("path")
            .attr("d", arc)
            .style("fill", (d, i) => colorScale(i))
            .style("stroke", "#fff")
            .style("stroke-width", "2px")
            .style("opacity", 0)
            .on("mouseover", function(event, d) {
                d3.select(this)
                    .style("opacity", 1)
                    .style("filter", "drop-shadow(0px 0px 10px rgba(0, 0, 0, 0.5))");
                
                // Show tooltip
                const tooltip = d3.select("body").append("div")
                    .attr("class", "d3-tooltip")
                    .style("position", "absolute")
                    .style("background", "rgba(0, 0, 0, 0.8)")
                    .style("color", "white")
                    .style("padding", "10px")
                    .style("border-radius", "5px")
                    .style("font-size", "12px")
                    .style("pointer-events", "none")
                    .style("z-index", "1000");
                
                tooltip.html(`${title}<br/>${d.data.name}: ${d.data.value}${unit} (${Math.round((d.data.value / total) * 100)}%)`)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 10) + "px");
            })
            .on("mouseout", function(event, d) {
                d3.select(this)
                    .style("opacity", 0.9)
                    .style("filter", "none");
                
                // Remove tooltip
                d3.selectAll(".d3-tooltip").remove();
            })
            .transition()
            .duration(750)
            .delay((d, i) => i * 100)
            .style("opacity", 0.9);
        
        // Add polylines for labels - connect all slices
        const polylines = g.selectAll("polyline")
            .data(pie(data)) // Connect all slices
            .enter().append("polyline")
            .style("fill", "none")
            .style("stroke", "#333")
            .style("stroke-width", "1px")
            .style("opacity", 0)
            .attr("points", d => {
                const centroid = arc.centroid(d);
                const labelPos = labelArc.centroid(d);
                const outerPos = [labelPos[0] * 1.2, labelPos[1] * 1.2];
                return [centroid, labelPos, outerPos].map(p => p.join(",")).join(" ");
            })
            .transition()
            .duration(1000)
            .delay((d, i) => i * 100)
            .style("opacity", 0.7);
        
        // Add labels outside the chart with connecting lines
        const labelRadius = outerRadius + 25;
        
        // Show labels for all processes
        const pieData = pie(data);
        const labelData = pieData; // Show all labels
        
        const labels = g.selectAll("text.label")
            .data(labelData)
            .enter().append("text")
            .attr("class", "label label-text")
            .attr("transform", d => {
                const angle = (d.startAngle + d.endAngle) / 2;
                const x = Math.cos(angle - Math.PI/2) * labelRadius;
                const y = Math.sin(angle - Math.PI/2) * labelRadius;
                return `translate(${x},${y})`;
            })
            .style("text-anchor", d => {
                const angle = (d.startAngle + d.endAngle) / 2;
                return angle > Math.PI ? "end" : "start";
            })
            .style("font-size", "10px")
            .style("fill", "#444")
            .style("font-weight", "500")
            .style("text-shadow", "1px 1px 2px rgba(255,255,255,0.8)")
            .style("opacity", 0)
            .each(function(d) {
                const name = d.data.name.length > 8 ? d.data.name.substring(0, 8) + '...' : d.data.name;
                const lines = [name, `${d.data.value}${unit}`];
                
                d3.select(this).selectAll('tspan')
                    .data(lines)
                    .enter()
                    .append('tspan')
                    .attr('x', 0)
                    .attr('dy', (_, i) => i === 0 ? 0 : '1.1em')
                    .text(d => d);
            })
            .transition()
            .duration(1000)
            .delay((d, i) => i * 200)
            .style("opacity", 1);
    }
    
    async loadChartData(endpoint) {
        try {
            console.log(`📡 Loading data from /api/${endpoint}...`);
            const response = await fetch(`/api/${endpoint}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            console.log(`✅ Data loaded from ${endpoint}:`, result);
            
            if (result.success) {
                return result;
            } else {
                throw new Error(result.error || 'Failed to load data');
            }
        } catch (error) {
            console.error(`❌ Error loading ${endpoint} data:`, error);
            return { success: false, error: error.message };
        }
    }
    
    showLoading(chartId) {
        const element = document.getElementById(chartId);
        element.innerHTML = '<div class="loading">Loading chart data...</div>';
    }
    
    showError(chartId, message) {
        const element = document.getElementById(chartId);
        element.innerHTML = `<div class="error">Error: ${message}</div>`;
    }
    
    async refreshChart(chartType) {
        console.log(`🔄 Refreshing chart: ${chartType}`);
        let endpoint, chartKey, chartId, unit = 'MB';
        
        switch (chartType) {
            case 'memory-monitoring':
                endpoint = 'memory-monitoring';
                chartKey = 'memoryMonitoring';
                chartId = 'memory-monitoring-chart';
                break;
            case 'memory-snapshot':
                endpoint = 'memory-snapshot';
                chartKey = 'memorySnapshot';
                chartId = 'memory-snapshot-chart';
                break;
            case 'cpu-usage':
                endpoint = 'cpu-usage';
                chartKey = 'cpuUsage';
                chartId = 'cpu-usage-chart';
                unit = '%';
                break;
            default:
                console.error('❌ Unknown chart type:', chartType);
                return;
        }
        
        this.showLoading(chartId);
        
        const result = await this.loadChartData(endpoint);
        console.log(`📊 Chart data for ${chartType}:`, result);
        
        if (result.success && result.data.length > 0) {
            console.log(`🎨 Creating D3.js chart for ${chartType}`);
            
            const containerElement = document.getElementById(chartId);
            if (containerElement) {
                this.createNightingaleChart(result.data, result.title, containerElement, unit);
                this.updateTimestamp(result.timestamp);
                console.log(`✅ Chart ${chartType} updated successfully`);
            } else {
                console.error(`❌ Container ${chartId} not found`);
                this.showError(chartId, 'Chart container not found');
            }
        } else {
            console.log(`⚠️ No data or error for ${chartType}:`, result);
            this.showError(chartId, result.error || 'No data available');
        }
    }
    
    async refreshAllCharts() {
        const chartTypes = ['memory-monitoring', 'memory-snapshot', 'cpu-usage'];
        
        // Refresh charts in parallel
        const promises = chartTypes.map(chartType => this.refreshChart(chartType));
        await Promise.all(promises);
        
        // Also refresh summary stats
        await this.loadSummaryStats();
    }
    
    async loadSummaryStats() {
        try {
            const result = await this.loadChartData('process-summary');
            
            if (result.success) {
                const data = result.data;
                
                // Update stats
                document.getElementById('total-processes').textContent = 
                    data.monitoring.total_processes || 0;
                document.getElementById('total-memory').textContent = 
                    Math.round(data.monitoring.total_memory || 0);
                document.getElementById('total-cpu').textContent = 
                    Math.round((data.monitoring.total_cpu || 0) * 100) / 100;
                
                this.updateTimestamp(result.timestamp);
            }
        } catch (error) {
            console.error('Error loading summary stats:', error);
        }
    }
    
    updateTimestamp(timestamp) {
        const date = new Date(timestamp);
        const timeString = date.toLocaleTimeString();
        document.getElementById('last-updated').textContent = timeString;
    }
    
    toggleAutoRefresh() {
        if (this.isAutoRefreshEnabled) {
            this.stopAutoRefresh();
        } else {
            this.startAutoRefresh();
        }
    }
    
    startAutoRefresh() {
        this.isAutoRefreshEnabled = true;
        document.getElementById('auto-refresh-status').textContent = 'Auto-refresh: ON';
        
        this.autoRefreshInterval = setInterval(() => {
            this.refreshAllCharts();
        }, this.refreshIntervalTime);
        
        console.log('Auto-refresh started');
    }
    
    stopAutoRefresh() {
        this.isAutoRefreshEnabled = false;
        document.getElementById('auto-refresh-status').textContent = 'Auto-refresh: OFF';
        
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
            this.autoRefreshInterval = null;
        }
        
        console.log('Auto-refresh stopped');
    }
    
    // Cleanup method
    destroy() {
        this.stopAutoRefresh();
        Object.keys(this.charts).forEach(chartKey => {
            const chartElement = this.charts[chartKey];
            if (chartElement && chartElement.element) {
                d3.select(chartElement.element).selectAll("*").remove();
            }
        });
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('🌟 DOM loaded, initializing dashboard...');
    
    // Wait a bit for D3.js to load if needed
    const initDashboard = () => {
        if (typeof d3 !== 'undefined') {
            console.log('✅ D3.js detected, creating dashboard...');
            window.dashboard = new TaskMonitorDashboard();
        } else {
            console.log('⏳ D3.js not ready, waiting...');
            setTimeout(initDashboard, 100);
        }
    };
    
    initDashboard();
});

// Cleanup when page is unloaded
window.addEventListener('beforeunload', () => {
    if (window.dashboard) {
        window.dashboard.destroy();
    }
});

// Handle visibility change to optimize performance
document.addEventListener('visibilitychange', () => {
    if (window.dashboard) {
        if (document.hidden) {
            window.dashboard.stopAutoRefresh();
        } else {
            // Optionally restart auto-refresh when page becomes visible
            // window.dashboard.startAutoRefresh();
        }
    }
});