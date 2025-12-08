// Market Analysis Page - Data Visualization and Interactions

let forecastChart = null;
let scatterChart = null;

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, checking Chart.js availability...');
    
    // Check if Chart.js is available
    if (typeof Chart === 'undefined') {
        console.error('Chart.js is not loaded!');
        return;
    }
    
    console.log('Chart.js is available, version:', Chart.version);
    
    // Initialize charts with a small delay to ensure DOM is ready
    setTimeout(() => {
        console.log('Starting chart initialization...');
        
        // Test canvas elements
        const forecastCanvas = document.getElementById('forecast-chart');
        const scatterCanvas = document.getElementById('scatter-chart');
        
        console.log('Forecast canvas found:', !!forecastCanvas);
        console.log('Scatter canvas found:', !!scatterCanvas);
        
        if (forecastCanvas) {
            console.log('Forecast canvas dimensions:', forecastCanvas.width, 'x', forecastCanvas.height);
        }
        if (scatterCanvas) {
            console.log('Scatter canvas dimensions:', scatterCanvas.width, 'x', scatterCanvas.height);
        }
        
        initForecastChart();
        initScatterChart();
        initInteractions();
        initCorrelationNetwork();
        
        // Initialize with default data
        console.log('Market Analysis page initialized');
    }, 500);
});

// Initialize Forecast Chart (Prophet-style)
function initForecastChart() {
    const ctx = document.getElementById('forecast-chart');
    if (!ctx) {
        console.error('Forecast chart canvas not found');
        return;
    }

    console.log('Initializing forecast chart...');

    try {
        // Simple test data first
        const labels = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
        const historicalData = [800, 850, 920, 980, 1050, 1100];
        const forecastData = [null, null, null, null, null, null, 1150, 1200, 1280, 1350, 1420, 1500];

        forecastChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Historical Data',
                        data: [...historicalData, ...Array(6).fill(null)],
                        borderColor: 'rgb(0, 212, 255)',
                        backgroundColor: 'rgba(0, 212, 255, 0.1)',
                        borderWidth: 3,
                        pointRadius: 4,
                        tension: 0.4
                    },
                    {
                        label: 'Forecast',
                        data: [...Array(6).fill(null), ...forecastData.slice(6)],
                        borderColor: 'rgb(0, 255, 136)',
                        backgroundColor: 'rgba(0, 255, 136, 0.1)',
                        borderWidth: 3,
                        borderDash: [5, 5],
                        pointRadius: 4,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: function(value) {
                                return value + ' jobs';
                            }
                        }
                    }
                }
            }
        });
        
        console.log('Forecast chart initialized successfully');
    } catch (error) {
        console.error('Error initializing forecast chart:', error);
    }
}

// Initialize Scatter Chart (Salary vs Demand)
function initScatterChart() {
    const ctx = document.getElementById('scatter-chart');
    if (!ctx) {
        console.error('Scatter chart canvas not found');
        return;
    }

    console.log('Initializing scatter chart...');

    const scatterData = generateScatterData();

    try {
        scatterChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'High Demand, High Salary',
                    data: scatterData.highHigh,
                    backgroundColor: 'rgba(0, 255, 136, 0.7)',
                    borderColor: 'rgb(0, 255, 136)',
                    borderWidth: 2,
                    pointRadius: 8,
                    pointHoverRadius: 12
                },
                {
                    label: 'High Demand, Lower Salary',
                    data: scatterData.highLow,
                    backgroundColor: 'rgba(255, 217, 61, 0.7)',
                    borderColor: 'rgb(255, 217, 61)',
                    borderWidth: 2,
                    pointRadius: 8,
                    pointHoverRadius: 12
                },
                {
                    label: 'Lower Demand, High Salary',
                    data: scatterData.lowHigh,
                    backgroundColor: 'rgba(0, 212, 255, 0.7)',
                    borderColor: 'rgb(0, 212, 255)',
                    borderWidth: 2,
                    pointRadius: 8,
                    pointHoverRadius: 12
                },
                {
                    label: 'Lower Demand, Lower Salary',
                    data: scatterData.lowLow,
                    backgroundColor: 'rgba(255, 107, 107, 0.7)',
                    borderColor: 'rgb(255, 107, 107)',
                    borderWidth: 2,
                    pointRadius: 8,
                    pointHoverRadius: 12
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 26, 26, 0.95)',
                    titleColor: '#00ff88',
                    bodyColor: '#ffffff',
                    borderColor: '#00ff88',
                    borderWidth: 1,
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            const point = context.raw;
                            return [
                                `Skill: ${point.label}`,
                                `Demand: ${point.x} jobs`,
                                `Avg Salary: $${point.y}k`
                            ];
                        }
                    }
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Job Demand (Number of Postings)',
                        color: '#a0a0a0',
                        font: {
                            family: 'Inter',
                            size: 14
                        }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#a0a0a0',
                        font: {
                            family: 'Inter'
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Average Salary ($k)',
                        color: '#a0a0a0',
                        font: {
                            family: 'Inter',
                            size: 14
                        }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#a0a0a0',
                        font: {
                            family: 'Inter'
                        },
                        callback: function(value) {
                            return '$' + value + 'k';
                        }
                    }
                }
            },
            onHover: (event, activeElements) => {
                event.native.target.style.cursor = activeElements.length > 0 ? 'pointer' : 'default';
            },
            onClick: (event, activeElements) => {
                if (activeElements.length > 0) {
                    const point = activeElements[0];
                    const dataPoint = scatterChart.data.datasets[point.datasetIndex].data[point.index];
                    showSkillDetail(dataPoint.label, dataPoint.x, dataPoint.y);
                }
            }
        }
    });

    // Add quadrant lines
    addQuadrantLines();
    
    console.log('Scatter chart initialized successfully');
    } catch (error) {
        console.error('Error initializing scatter chart:', error);
    }
}

// Show skill detail popup
function showSkillDetail(skillName, demand, salary) {
    alert(`Skill: ${skillName}\nDemand: ${demand} jobs\nAverage Salary: $${salary}k\n\nClick OK to explore jobs for this skill.`);
}

// Generate sample historical data
function generateHistoricalData() {
    const months = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const baseValue = 800;
    const values = months.map((_, i) => baseValue + Math.random() * 200 + i * 50);
    
    console.log('Generated historical data:', { labels: months, values });
    
    return {
        labels: months,
        values: values
    };
}

// Generate sample forecast data
function generateForecastData() {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
    const baseValue = 1100;
    const values = months.map((_, i) => baseValue + i * 70 + Math.random() * 100);
    const upper = values.map(v => v + 150);
    const lower = values.map(v => v - 100);
    
    console.log('Generated forecast data:', { labels: months, values, upper, lower });
    
    return {
        labels: months,
        values: values,
        upper: upper,
        lower: lower
    };
}

// Generate scatter plot data
function generateScatterData() {
    const data = {
        highHigh: [
            { x: 450, y: 145, label: 'AI/ML Engineer' },
            { x: 380, y: 155, label: 'Cloud Architect' },
            { x: 320, y: 140, label: 'Blockchain Dev' },
            { x: 290, y: 138, label: 'Security Engineer' }
        ],
        highLow: [
            { x: 520, y: 95, label: 'React Developer' },
            { x: 480, y: 88, label: 'Node.js Developer' },
            { x: 450, y: 92, label: 'Python Developer' },
            { x: 410, y: 85, label: 'Frontend Developer' }
        ],
        lowHigh: [
            { x: 120, y: 165, label: 'Rust Developer' },
            { x: 95, y: 158, label: 'Solidity Developer' },
            { x: 80, y: 170, label: 'Quantum Computing' },
            { x: 110, y: 148, label: 'Embedded Systems' }
        ],
        lowLow: [
            { x: 180, y: 65, label: 'jQuery Developer' },
            { x: 150, y: 58, label: 'PHP Developer' },
            { x: 90, y: 52, label: 'Flash Developer' },
            { x: 120, y: 60, label: 'Perl Developer' }
        ]
    };
    
    console.log('Generated scatter data:', data);
    return data;
}

// Add quadrant lines to scatter chart
function addQuadrantLines() {
    const showQuadrants = document.getElementById('show-quadrants');
    if (showQuadrants && showQuadrants.checked) {
        // This would be implemented with Chart.js annotation plugin
        console.log('Quadrant lines enabled');
    }
}

// Initialize all interactions
function initInteractions() {
    // Forecast button
    const forecastBtn = document.getElementById('forecast-btn');
    const skillSelect = document.getElementById('skill-select');
    
    if (forecastBtn) {
        forecastBtn.addEventListener('click', () => {
            const skill = skillSelect.value;
            updateForecast(skill);
        });
    }

    // Heatmap skill selector
    const heatmapSkillSelect = document.getElementById('heatmap-skill-select');
    if (heatmapSkillSelect) {
        heatmapSkillSelect.addEventListener('change', (e) => {
            updateHeatmap(e.target.value);
        });
        
        // Initialize with default skill
        updateHeatmap(heatmapSkillSelect.value);
    }

    // Heatmap cell interactions
    const heatmapCells = document.querySelectorAll('.heatmap-cell[data-value]');
    heatmapCells.forEach(cell => {
        cell.addEventListener('click', function() {
            const row = this.closest('.heatmap-row');
            const region = row.dataset.region;
            const value = this.querySelector('.cell-value')?.textContent;
            
            if (region && value) {
                showRegionDetail(region, value);
            }
        });
    });

    // Scatter chart controls
    const showLabels = document.getElementById('show-labels');
    const showQuadrants = document.getElementById('show-quadrants');
    
    if (showLabels) {
        showLabels.addEventListener('change', (e) => {
            toggleScatterLabels(e.target.checked);
        });
    }
    
    if (showQuadrants) {
        showQuadrants.addEventListener('change', (e) => {
            toggleQuadrants(e.target.checked);
        });
    }

    // Refresh correlation button
    const refreshBtn = document.getElementById('refresh-correlation');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            refreshCorrelationNetwork();
        });
    }
    
    // Initialize forecast with default skill
    if (skillSelect) {
        updateForecast(skillSelect.value);
    }
}

// Update forecast based on selected skill
async function updateForecast(skill) {
    console.log('Updating forecast for:', skill);
    
    try {
        // Show loading state
        const forecastBtn = document.getElementById('forecast-btn');
        forecastBtn.disabled = true;
        forecastBtn.textContent = 'Loading...';
        
        // Fetch real data from API
        const data = await api.getSkillForecast(skill, null, 180);
        
        if (data.message) {
            console.warn('API message:', data.message);
            // Use fallback data if no real data available
            updateForecastWithFallback(skill);
            return;
        }
        
        // Process historical data
        const historical = data.historical_points || [];
        const forecast = data.forecast_points || [];
        
        if (historical.length === 0 && forecast.length === 0) {
            console.warn('No data available, using fallback');
            updateForecastWithFallback(skill);
            return;
        }
        
        // Format data for chart
        const historicalLabels = historical.map(point => {
            const date = new Date(point.ds);
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        });
        
        const forecastLabels = forecast.map(point => {
            const date = new Date(point.ds);
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        });
        
        const historicalValues = historical.map(point => point.y);
        const forecastValues = forecast.map(point => point.yhat);
        const forecastUpper = forecast.map(point => point.yhat_upper);
        const forecastLower = forecast.map(point => point.yhat_lower);
        
        // Update chart
        forecastChart.data.labels = [...historicalLabels, ...forecastLabels];
        forecastChart.data.datasets[0].data = historicalValues;
        forecastChart.data.datasets[1].data = [...Array(historicalValues.length).fill(null), ...forecastValues];
        forecastChart.data.datasets[2].data = [...Array(historicalValues.length).fill(null), ...forecastUpper];
        forecastChart.data.datasets[3].data = [...Array(historicalValues.length).fill(null), ...forecastLower];
        
        forecastChart.update('active');
        
        // Update stats with real data
        updateForecastStatsFromAPI(skill, historical, forecast);
        
    } catch (error) {
        console.error('Error fetching forecast:', error);
        // Use fallback data when API is not available
        updateForecastWithFallback(skill);
    } finally {
        const forecastBtn = document.getElementById('forecast-btn');
        forecastBtn.disabled = false;
        forecastBtn.textContent = 'Generate Forecast';
    }
}

// Fallback function when API is not available
function updateForecastWithFallback(skill) {
    console.log('Using fallback data for skill:', skill);
    
    // Generate realistic sample data based on skill
    const skillData = getSkillFallbackData(skill);
    const historical = generateHistoricalDataForSkill(skill, skillData);
    const forecast = generateForecastDataForSkill(skill, skillData);
    
    // Update chart
    forecastChart.data.labels = [...historical.labels, ...forecast.labels];
    forecastChart.data.datasets[0].data = historical.values;
    forecastChart.data.datasets[1].data = [...Array(historical.values.length).fill(null), ...forecast.values];
    forecastChart.data.datasets[2].data = [...Array(historical.values.length).fill(null), ...forecast.upper];
    forecastChart.data.datasets[3].data = [...Array(historical.values.length).fill(null), ...forecast.lower];
    
    forecastChart.update('active');
    
    // Update stats
    updateForecastStats(skill, historical, forecast);
}

// Get skill-specific fallback data
function getSkillFallbackData(skill) {
    const skillProfiles = {
        'python': { base: 1200, growth: 0.25, volatility: 0.15 },
        'javascript': { base: 1500, growth: 0.20, volatility: 0.12 },
        'react': { base: 900, growth: 0.30, volatility: 0.18 },
        'ai-engineer': { base: 600, growth: 0.45, volatility: 0.25 },
        'devops': { base: 800, growth: 0.35, volatility: 0.20 },
        'aws': { base: 700, growth: 0.40, volatility: 0.22 },
        'data-science': { base: 850, growth: 0.28, volatility: 0.16 },
        'machine-learning': { base: 650, growth: 0.42, volatility: 0.24 }
    };
    
    return skillProfiles[skill] || { base: 800, growth: 0.25, volatility: 0.15 };
}

// Generate historical data for specific skill
function generateHistoricalDataForSkill(skill, skillData) {
    const months = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const { base, growth, volatility } = skillData;
    
    const values = months.map((_, i) => {
        const trend = base + (i * base * growth / 6);
        const noise = (Math.random() - 0.5) * base * volatility;
        return Math.max(50, Math.round(trend + noise));
    });
    
    return { labels: months, values };
}

// Generate forecast data for specific skill
function generateForecastDataForSkill(skill, skillData) {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
    const { base, growth, volatility } = skillData;
    
    const startValue = base * (1 + growth);
    const values = months.map((_, i) => {
        const trend = startValue + (i * startValue * growth / 6);
        const noise = (Math.random() - 0.5) * startValue * volatility * 0.5;
        return Math.max(50, Math.round(trend + noise));
    });
    
    const upper = values.map(v => Math.round(v * (1 + volatility)));
    const lower = values.map(v => Math.round(v * (1 - volatility * 0.7)));
    
    return { labels: months, values, upper, lower };
}

// Update forecast statistics from API data
function updateForecastStatsFromAPI(skill, historical, forecast) {
    if (historical.length === 0 || forecast.length === 0) return;
    
    const currentDemand = historical[historical.length - 1].y;
    const forecastDemand = forecast[forecast.length - 1].yhat;
    const growthRate = ((forecastDemand - currentDemand) / currentDemand * 100).toFixed(0);
    
    document.getElementById('growth-rate').textContent = `${growthRate > 0 ? '+' : ''}${growthRate}%`;
    document.getElementById('current-demand').textContent = `${Math.round(currentDemand)} jobs`;
    document.getElementById('forecast-demand').textContent = `${Math.round(forecastDemand)} jobs`;
    
    const trendIndicator = document.getElementById('trend-indicator');
    if (growthRate > 20) {
        trendIndicator.textContent = 'Strong Upward';
        trendIndicator.className = 'stat-value trend-up';
    } else if (growthRate > 10) {
        trendIndicator.textContent = 'Moderate Growth';
        trendIndicator.className = 'stat-value trend-up';
    } else if (growthRate > 0) {
        trendIndicator.textContent = 'Slight Growth';
        trendIndicator.className = 'stat-value';
    } else {
        trendIndicator.textContent = 'Declining';
        trendIndicator.className = 'stat-value trend-down';
    }
}

// Update forecast statistics
function updateForecastStats(skill, historical, forecast) {
    const currentDemand = historical.values[historical.values.length - 1];
    const forecastDemand = forecast.values[forecast.values.length - 1];
    const growthRate = ((forecastDemand - currentDemand) / currentDemand * 100).toFixed(0);
    
    document.getElementById('growth-rate').textContent = `+${growthRate}%`;
    document.getElementById('current-demand').textContent = `${Math.round(currentDemand)} jobs`;
    document.getElementById('forecast-demand').textContent = `${Math.round(forecastDemand)} jobs`;
    
    const trendIndicator = document.getElementById('trend-indicator');
    if (growthRate > 20) {
        trendIndicator.textContent = 'Strong Upward';
        trendIndicator.className = 'stat-value trend-up';
    } else if (growthRate > 10) {
        trendIndicator.textContent = 'Moderate Growth';
        trendIndicator.className = 'stat-value trend-up';
    } else if (growthRate > 0) {
        trendIndicator.textContent = 'Slight Growth';
        trendIndicator.className = 'stat-value';
    } else {
        trendIndicator.textContent = 'Declining';
        trendIndicator.className = 'stat-value trend-down';
    }
}

// Update heatmap based on selected skill
async function updateHeatmap(skill) {
    console.log('Updating heatmap for:', skill);
    
    try {
        // Show loading effect
        const cells = document.querySelectorAll('.heatmap-cell[data-value]');
        cells.forEach(cell => {
            cell.style.opacity = '0.5';
            cell.style.transition = 'opacity 0.3s ease';
        });
        
        // Get skill-specific data
        const skillHeatmapData = getHeatmapDataForSkill(skill);
        
        // Update each region row
        const regions = ['usa', 'india', 'uk', 'germany', 'canada', 'australia'];
        regions.forEach((region, regionIndex) => {
            const row = document.querySelector(`.heatmap-row[data-region="${region}"]`);
            if (!row) return;
            
            const dataCells = row.querySelectorAll('.heatmap-cell[data-value]');
            const growthCell = row.querySelector('.heatmap-cell.growth .growth-value');
            
            const regionData = skillHeatmapData[region];
            
            // Update data cells
            dataCells.forEach((cell, cellIndex) => {
                if (cellIndex < regionData.values.length) {
                    const value = regionData.values[cellIndex];
                    const intensity = regionData.intensities[cellIndex];
                    
                    cell.querySelector('.cell-value').textContent = value.toLocaleString();
                    cell.setAttribute('data-value', intensity);
                    
                    // Update background color based on intensity
                    cell.style.background = `rgba(0, 255, 136, ${intensity / 100})`;
                }
            });
            
            // Update growth percentage
            if (growthCell) {
                growthCell.textContent = `+${regionData.growth}%`;
            }
        });
        
        // Restore opacity
        setTimeout(() => {
            cells.forEach(cell => {
                cell.style.opacity = '1';
            });
        }, 500);
        
    } catch (error) {
        console.error('Error updating heatmap:', error);
        // Restore opacity even on error
        const cells = document.querySelectorAll('.heatmap-cell[data-value]');
        cells.forEach(cell => {
            cell.style.opacity = '1';
        });
    }
}

// Get heatmap data for specific skill
function getHeatmapDataForSkill(skill) {
    const skillHeatmapProfiles = {
        'data-science': {
            usa: { values: [1245, 1380, 1544], intensities: [85, 92, 98], growth: 24 },
            india: { values: [892, 1045, 1234], intensities: [78, 88, 95], growth: 38 },
            uk: { values: [567, 612, 678], intensities: [72, 75, 80], growth: 20 },
            germany: { values: [445, 478, 512], intensities: [68, 70, 73], growth: 15 },
            canada: { values: [389, 423, 467], intensities: [65, 68, 72], growth: 20 },
            australia: { values: [312, 334, 356], intensities: [60, 62, 65], growth: 14 }
        },
        'python': {
            usa: { values: [1580, 1720, 1890], intensities: [88, 94, 99], growth: 20 },
            india: { values: [1120, 1290, 1450], intensities: [82, 90, 96], growth: 29 },
            uk: { values: [680, 720, 780], intensities: [75, 78, 82], growth: 15 },
            germany: { values: [520, 560, 600], intensities: [70, 73, 76], growth: 15 },
            canada: { values: [450, 490, 530], intensities: [68, 71, 74], growth: 18 },
            australia: { values: [380, 410, 440], intensities: [63, 66, 69], growth: 16 }
        },
        'react': {
            usa: { values: [2100, 2350, 2650], intensities: [92, 97, 100], growth: 26 },
            india: { values: [1450, 1680, 1920], intensities: [85, 92, 98], growth: 32 },
            uk: { values: [890, 950, 1020], intensities: [78, 81, 85], growth: 15 },
            germany: { values: [670, 720, 780], intensities: [73, 76, 80], growth: 16 },
            canada: { values: [580, 630, 690], intensities: [71, 74, 78], growth: 19 },
            australia: { values: [490, 530, 580], intensities: [67, 70, 74], growth: 18 }
        },
        'devops': {
            usa: { values: [980, 1120, 1290], intensities: [82, 89, 95], growth: 32 },
            india: { values: [720, 850, 990], intensities: [76, 84, 91], growth: 38 },
            uk: { values: [450, 490, 540], intensities: [69, 72, 76], growth: 20 },
            germany: { values: [380, 420, 470], intensities: [66, 69, 73], growth: 24 },
            canada: { values: [320, 360, 410], intensities: [63, 66, 70], growth: 28 },
            australia: { values: [280, 310, 350], intensities: [60, 63, 67], growth: 25 }
        }
    };
    
    return skillHeatmapProfiles[skill] || skillHeatmapProfiles['data-science'];
}

// Show region detail popup
function showRegionDetail(region, value) {
    alert(`Region: ${region}\nJob Count: ${value}\n\nClick OK to explore jobs in this region.`);
}

// Toggle scatter chart labels
function toggleScatterLabels(show) {
    if (scatterChart) {
        scatterChart.options.plugins.tooltip.enabled = show;
        scatterChart.update();
    }
}

// Toggle quadrant lines
function toggleQuadrants(show) {
    console.log('Quadrants:', show ? 'shown' : 'hidden');
    // Would implement with Chart.js annotation plugin
}

// Initialize correlation network interactions
function initCorrelationNetwork() {
    const nodes = document.querySelectorAll('.correlation-node');
    
    nodes.forEach(node => {
        node.addEventListener('mouseenter', function() {
            const circle = this.querySelector('circle');
            const originalR = circle.getAttribute('r');
            circle.setAttribute('data-original-r', originalR);
            circle.setAttribute('r', parseFloat(originalR) * 1.15);
            
            // Highlight connected edges
            highlightConnectedEdges(this, true);
        });
        
        node.addEventListener('mouseleave', function() {
            const circle = this.querySelector('circle');
            const originalR = circle.getAttribute('data-original-r');
            if (originalR) {
                circle.setAttribute('r', originalR);
            }
            
            // Reset edges
            highlightConnectedEdges(this, false);
        });
        
        node.addEventListener('click', function() {
            const skill = this.dataset.skill;
            showSkillCorrelationDetail(skill);
        });
    });
}

// Highlight edges connected to a node
function highlightConnectedEdges(node, highlight) {
    const edges = document.querySelectorAll('.correlation-edge');
    edges.forEach(edge => {
        if (highlight) {
            edge.style.stroke = 'var(--accent-green)';
            edge.style.strokeWidth = '5';
        } else {
            edge.style.stroke = '';
            edge.style.strokeWidth = '';
        }
    });
}

// Show skill correlation details
function showSkillCorrelationDetail(skill) {
    console.log('Showing correlation details for:', skill);
    
    // In production, fetch from API:
    // fetch(`/api/ml/skill-correlations?skill=${skill}`)
    //     .then(res => res.json())
    //     .then(data => displayCorrelationData(data));
    
    alert(`Skill: ${skill}\n\nRelated Skills:\n- Machine Learning\n- Data Science\n- TensorFlow\n- PyTorch\n\nClick OK to view related jobs.`);
}

// Refresh correlation network based on selected skill
async function refreshCorrelationNetwork() {
    console.log('Refreshing correlation network...');
    
    try {
        // Get the currently selected skill from forecast section
        const skillSelect = document.getElementById('skill-select');
        const selectedSkill = skillSelect ? skillSelect.value : 'python';
        
        // Add animation effect
        const graph = document.getElementById('correlation-graph');
        graph.style.opacity = '0.5';
        graph.style.transition = 'opacity 0.5s ease';
        
        // Try to fetch from API first
        try {
            const correlationData = await api.getSkillCorrelations(null, 15);
            updateCorrelationNetworkFromAPI(correlationData, selectedSkill);
        } catch (error) {
            console.warn('API not available, using fallback correlation data');
            updateCorrelationNetworkFallback(selectedSkill);
        }
        
        // Update network info
        updateCorrelationInfo(selectedSkill);
        
        setTimeout(() => {
            graph.style.opacity = '1';
        }, 500);
        
    } catch (error) {
        console.error('Error refreshing correlation network:', error);
        const graph = document.getElementById('correlation-graph');
        graph.style.opacity = '1';
    }
}

// Update correlation network from API data
function updateCorrelationNetworkFromAPI(data, centralSkill) {
    console.log('Updating correlation network with API data for:', centralSkill);
    // This would update the SVG based on real correlation data
    // For now, fall back to the static update
    updateCorrelationNetworkFallback(centralSkill);
}

// Update correlation network with fallback data
function updateCorrelationNetworkFallback(centralSkill) {
    console.log('Updating correlation network for central skill:', centralSkill);
    
    // Get skill-specific correlation data
    const correlationData = getCorrelationDataForSkill(centralSkill);
    
    // Update central node
    const centralNode = document.querySelector('.correlation-node.central');
    if (centralNode) {
        const centralText = centralNode.querySelector('.node-label-large');
        if (centralText) {
            centralText.textContent = correlationData.central.name;
        }
        centralNode.setAttribute('data-skill', correlationData.central.name);
    }
    
    // Update connected nodes
    const nodes = document.querySelectorAll('.correlation-node:not(.central)');
    nodes.forEach((node, index) => {
        if (index < correlationData.connected.length) {
            const skillData = correlationData.connected[index];
            const text = node.querySelector('.node-label, .node-label-small');
            if (text) {
                text.textContent = skillData.name;
            }
            node.setAttribute('data-skill', skillData.name);
            
            // Update circle color based on category
            const circle = node.querySelector('circle');
            if (circle) {
                circle.setAttribute('fill', skillData.color);
            }
        }
    });
}

// Get correlation data for specific skill
function getCorrelationDataForSkill(skill) {
    const correlationProfiles = {
        'python': {
            central: { name: 'Python', color: 'var(--accent-green)' },
            connected: [
                { name: 'Django', color: '#ff6b6b' },
                { name: 'Flask', color: '#ff6b6b' },
                { name: 'Pandas', color: '#ffd93d' },
                { name: 'NumPy', color: '#ffd93d' },
                { name: 'ML', color: 'var(--accent-blue)' },
                { name: 'Data Sci', color: 'var(--accent-blue)' },
                { name: 'TensorFlow', color: '#a78bfa' },
                { name: 'PyTorch', color: '#a78bfa' },
                { name: 'Scikit', color: '#a78bfa' },
                { name: 'SQL', color: '#6ee7b7' }
            ]
        },
        'javascript': {
            central: { name: 'JavaScript', color: 'var(--accent-green)' },
            connected: [
                { name: 'React', color: '#ff6b6b' },
                { name: 'Vue.js', color: '#ff6b6b' },
                { name: 'Node.js', color: '#ffd93d' },
                { name: 'Express', color: '#ffd93d' },
                { name: 'Frontend', color: 'var(--accent-blue)' },
                { name: 'Backend', color: 'var(--accent-blue)' },
                { name: 'TypeScript', color: '#a78bfa' },
                { name: 'Angular', color: '#a78bfa' },
                { name: 'MongoDB', color: '#6ee7b7' },
                { name: 'REST API', color: '#6ee7b7' }
            ]
        },
        'react': {
            central: { name: 'React', color: 'var(--accent-green)' },
            connected: [
                { name: 'JavaScript', color: '#ff6b6b' },
                { name: 'TypeScript', color: '#ff6b6b' },
                { name: 'Redux', color: '#ffd93d' },
                { name: 'Next.js', color: '#ffd93d' },
                { name: 'Frontend', color: 'var(--accent-blue)' },
                { name: 'UI/UX', color: 'var(--accent-blue)' },
                { name: 'CSS', color: '#a78bfa' },
                { name: 'HTML', color: '#a78bfa' },
                { name: 'Webpack', color: '#6ee7b7' },
                { name: 'Jest', color: '#6ee7b7' }
            ]
        },
        'ai-engineer': {
            central: { name: 'AI Engineer', color: 'var(--accent-green)' },
            connected: [
                { name: 'Python', color: '#ff6b6b' },
                { name: 'TensorFlow', color: '#ff6b6b' },
                { name: 'PyTorch', color: '#ffd93d' },
                { name: 'Keras', color: '#ffd93d' },
                { name: 'ML', color: 'var(--accent-blue)' },
                { name: 'Deep Learn', color: 'var(--accent-blue)' },
                { name: 'NLP', color: '#a78bfa' },
                { name: 'Computer Vision', color: '#a78bfa' },
                { name: 'MLOps', color: '#6ee7b7' },
                { name: 'Cloud AI', color: '#6ee7b7' }
            ]
        },
        'devops': {
            central: { name: 'DevOps', color: 'var(--accent-green)' },
            connected: [
                { name: 'Docker', color: '#ff6b6b' },
                { name: 'Kubernetes', color: '#ff6b6b' },
                { name: 'AWS', color: '#ffd93d' },
                { name: 'Azure', color: '#ffd93d' },
                { name: 'CI/CD', color: 'var(--accent-blue)' },
                { name: 'Jenkins', color: 'var(--accent-blue)' },
                { name: 'Terraform', color: '#a78bfa' },
                { name: 'Ansible', color: '#a78bfa' },
                { name: 'Linux', color: '#6ee7b7' },
                { name: 'Monitoring', color: '#6ee7b7' }
            ]
        },
        'aws': {
            central: { name: 'AWS', color: 'var(--accent-green)' },
            connected: [
                { name: 'EC2', color: '#ff6b6b' },
                { name: 'S3', color: '#ff6b6b' },
                { name: 'Lambda', color: '#ffd93d' },
                { name: 'RDS', color: '#ffd93d' },
                { name: 'Cloud', color: 'var(--accent-blue)' },
                { name: 'DevOps', color: 'var(--accent-blue)' },
                { name: 'Terraform', color: '#a78bfa' },
                { name: 'Docker', color: '#a78bfa' },
                { name: 'Python', color: '#6ee7b7' },
                { name: 'Linux', color: '#6ee7b7' }
            ]
        },
        'data-science': {
            central: { name: 'Data Science', color: 'var(--accent-green)' },
            connected: [
                { name: 'Python', color: '#ff6b6b' },
                { name: 'R', color: '#ff6b6b' },
                { name: 'Pandas', color: '#ffd93d' },
                { name: 'NumPy', color: '#ffd93d' },
                { name: 'ML', color: 'var(--accent-blue)' },
                { name: 'Statistics', color: 'var(--accent-blue)' },
                { name: 'Jupyter', color: '#a78bfa' },
                { name: 'Matplotlib', color: '#a78bfa' },
                { name: 'SQL', color: '#6ee7b7' },
                { name: 'Tableau', color: '#6ee7b7' }
            ]
        },
        'machine-learning': {
            central: { name: 'Machine Learning', color: 'var(--accent-green)' },
            connected: [
                { name: 'Python', color: '#ff6b6b' },
                { name: 'Scikit', color: '#ff6b6b' },
                { name: 'TensorFlow', color: '#ffd93d' },
                { name: 'PyTorch', color: '#ffd93d' },
                { name: 'Data Sci', color: 'var(--accent-blue)' },
                { name: 'AI', color: 'var(--accent-blue)' },
                { name: 'Deep Learn', color: '#a78bfa' },
                { name: 'NLP', color: '#a78bfa' },
                { name: 'Statistics', color: '#6ee7b7' },
                { name: 'Algorithms', color: '#6ee7b7' }
            ]
        }
    };
    
    return correlationProfiles[skill] || correlationProfiles['python'];
}

// Update correlation info panel
function updateCorrelationInfo(skill) {
    const infoItems = document.querySelectorAll('.correlation-info .info-item');
    
    // Update based on skill
    const skillStats = {
        'python': { skills: 18, connections: 28, strongest: 'Python + Data Science' },
        'javascript': { skills: 16, connections: 25, strongest: 'JavaScript + React' },
        'react': { skills: 14, connections: 22, strongest: 'React + JavaScript' },
        'ai-engineer': { skills: 20, connections: 32, strongest: 'AI + Machine Learning' },
        'devops': { skills: 17, connections: 26, strongest: 'DevOps + AWS' },
        'aws': { skills: 15, connections: 24, strongest: 'AWS + DevOps' },
        'data-science': { skills: 19, connections: 30, strongest: 'Data Science + Python' },
        'machine-learning': { skills: 21, connections: 34, strongest: 'ML + Python' }
    };
    
    const stats = skillStats[skill] || skillStats['python'];
    
    if (infoItems.length >= 3) {
        infoItems[0].querySelector('.info-value').textContent = stats.skills;
        infoItems[1].querySelector('.info-value').textContent = stats.connections;
        infoItems[2].querySelector('.info-value').textContent = stats.strongest;
    }
}

// Animate elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe sections
document.querySelectorAll('.forecast-section, .heatmap-section, .correlation-section, .scatter-section').forEach(section => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(30px)';
    section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(section);
});

// Animate stat boxes
const statBoxes = document.querySelectorAll('.stat-box');
statBoxes.forEach((box, index) => {
    box.style.transitionDelay = `${index * 0.1}s`;
});
