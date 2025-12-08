// Job Discovery Page Interactive Features

document.addEventListener('DOMContentLoaded', () => {
    initViewToggle();
    initMapView();
    initGraphView();
    initFilters();
});

// View Toggle Functionality
function initViewToggle() {
    const toggleButtons = document.querySelectorAll('.toggle-btn');
    const mapView = document.getElementById('map-view');
    const graphView = document.getElementById('graph-view');
    const instructionText = document.getElementById('instruction-text');

    toggleButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const view = btn.dataset.view;
            
            // Update active button
            toggleButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Switch views
            if (view === 'map') {
                mapView.classList.add('active');
                graphView.classList.remove('active');
                instructionText.textContent = 'Hover over regions to see job density. Click to explore detailed insights.';
            } else {
                graphView.classList.add('active');
                mapView.classList.remove('active');
                instructionText.textContent = 'Click on skill nodes to see connections. Node size represents relevance.';
            }
        });
    });
}

// Map View Interactions
function initMapView() {
    const regionMarkers = document.querySelectorAll('.region-marker');
    const regionCard = document.getElementById('region-card');
    const cardClose = regionCard.querySelector('.card-close');

    const regionData = {
        'North America': {
            jobs: '1,245',
            growth: '+15%',
            roles: ['Software Engineer', 'Data Scientist', 'Product Manager']
        },
        'Europe': {
            jobs: '892',
            growth: '+12%',
            roles: ['Full Stack Developer', 'DevOps Engineer', 'UX Designer']
        },
        'Asia': {
            jobs: '1,567',
            growth: '+22%',
            roles: ['Backend Developer', 'Mobile Developer', 'Cloud Architect']
        },
        'South America': {
            jobs: '234',
            growth: '+8%',
            roles: ['Frontend Developer', 'QA Engineer', 'Scrum Master']
        },
        'Africa': {
            jobs: '312',
            growth: '+18%',
            roles: ['Software Developer', 'Data Analyst', 'Project Manager']
        },
        'Australia': {
            jobs: '456',
            growth: '+10%',
            roles: ['Full Stack Engineer', 'Security Engineer', 'Tech Lead']
        }
    };

    regionMarkers.forEach(marker => {
        marker.addEventListener('mouseenter', function() {
            this.style.opacity = '1';
            this.style.transform = 'scale(1.15)';
        });

        marker.addEventListener('mouseleave', function() {
            const density = this.classList.contains('high-density') ? '0.7' : 
                           this.classList.contains('medium-density') ? '0.6' : '0.5';
            this.style.opacity = density;
            this.style.transform = 'scale(1)';
        });

        marker.addEventListener('click', function() {
            const region = this.dataset.region;
            const data = regionData[region];
            
            if (data) {
                showRegionCard(region, data);
            }
        });
    });

    cardClose.addEventListener('click', () => {
        regionCard.style.display = 'none';
    });

    function showRegionCard(region, data) {
        document.getElementById('region-name').textContent = region;
        document.getElementById('region-jobs').textContent = data.jobs;
        document.getElementById('region-growth').textContent = data.growth;
        
        const rolesList = document.getElementById('region-roles');
        rolesList.innerHTML = data.roles.map(role => `<li>${role}</li>`).join('');
        
        regionCard.style.display = 'block';
    }
}

// Graph View Interactions
function initGraphView() {
    const skillNodes = document.querySelectorAll('.skill-node');
    const skillCard = document.getElementById('skill-card');
    const cardClose = skillCard.querySelector('.card-close');

    const skillData = {
        'React': {
            jobs: '342',
            salary: '$125k',
            related: ['JavaScript', 'TypeScript', 'Redux', 'Next.js']
        },
        'Node.js': {
            jobs: '298',
            salary: '$118k',
            related: ['Express', 'MongoDB', 'REST API', 'GraphQL']
        },
        'Python': {
            jobs: '456',
            salary: '$132k',
            related: ['Django', 'Flask', 'Pandas', 'NumPy']
        },
        'AWS': {
            jobs: '387',
            salary: '$145k',
            related: ['EC2', 'S3', 'Lambda', 'CloudFormation']
        },
        'Docker': {
            jobs: '234',
            salary: '$128k',
            related: ['Kubernetes', 'CI/CD', 'Jenkins', 'GitLab']
        },
        'MongoDB': {
            jobs: '189',
            salary: '$115k',
            related: ['NoSQL', 'Mongoose', 'Atlas', 'Aggregation']
        }
    };

    skillNodes.forEach(node => {
        node.addEventListener('mouseenter', function() {
            const circle = this.querySelector('circle');
            circle.style.transform = 'scale(1.15)';
            
            // Highlight connected edges
            const edges = document.querySelectorAll('.edge');
            edges.forEach(edge => {
                edge.style.stroke = 'var(--accent-green)';
                edge.style.strokeWidth = '3';
            });
        });

        node.addEventListener('mouseleave', function() {
            const circle = this.querySelector('circle');
            circle.style.transform = 'scale(1)';
            
            // Reset edges
            const edges = document.querySelectorAll('.edge');
            edges.forEach(edge => {
                edge.style.stroke = 'var(--border-color)';
                edge.style.strokeWidth = '2';
            });
        });

        node.addEventListener('click', function() {
            const skill = this.dataset.skill;
            const data = skillData[skill];
            
            if (data) {
                showSkillCard(skill, data);
            }
        });
    });

    // Central node interaction
    const centralNode = document.querySelector('.central-node');
    if (centralNode) {
        centralNode.addEventListener('click', function() {
            showSkillCard('Full Stack Development', {
                jobs: '567',
                salary: '$135k',
                related: ['React', 'Node.js', 'Python', 'AWS', 'Docker', 'MongoDB']
            });
        });
    }

    cardClose.addEventListener('click', () => {
        skillCard.style.display = 'none';
    });

    function showSkillCard(skill, data) {
        document.getElementById('skill-name').textContent = skill;
        document.getElementById('skill-jobs').textContent = data.jobs;
        document.getElementById('skill-salary').textContent = data.salary;
        
        const relatedSkills = document.getElementById('related-skills');
        relatedSkills.innerHTML = data.related.map(s => 
            `<span class="skill-tag">${s}</span>`
        ).join('');
        
        skillCard.style.display = 'block';
    }
}

// Filter Interactions
function initFilters() {
    const skillInput = document.querySelector('.filter-input');
    const roleSelect = document.querySelector('.filter-select');
    const salarySlider = document.querySelector('.slider');
    const rangeValues = document.querySelector('.range-values');

    // Skill search with debounce
    let searchTimeout;
    skillInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const query = e.target.value.toLowerCase();
            console.log('Searching for skills:', query);
            // In production, this would filter the visualization
            updateSkillHighlights(query);
        }, 300);
    });

    // Role filter
    roleSelect.addEventListener('change', (e) => {
        const role = e.target.value;
        console.log('Filtering by role:', role);
        // In production, this would update the visualization
        updateRoleFilter(role);
    });

    // Salary range slider
    salarySlider.addEventListener('input', (e) => {
        const value = e.target.value;
        const maxSalary = value * 2; // Convert to thousands
        rangeValues.innerHTML = `
            <span>$0k</span>
            <span>$${maxSalary}k+</span>
        `;
        console.log('Salary range:', 0, '-', maxSalary);
        // In production, this would filter jobs by salary
    });
}

// Helper functions for filtering (placeholders for backend integration)
function updateSkillHighlights(query) {
    // This would highlight matching skills in the graph view
    const nodes = document.querySelectorAll('.skill-node');
    nodes.forEach(node => {
        const skill = node.dataset.skill.toLowerCase();
        if (query && skill.includes(query)) {
            node.querySelector('circle').style.stroke = 'var(--accent-green)';
            node.querySelector('circle').style.strokeWidth = '4';
        } else {
            node.querySelector('circle').style.stroke = 'var(--bg-dark)';
            node.querySelector('circle').style.strokeWidth = '3';
        }
    });
}

function updateRoleFilter(role) {
    // This would filter the map/graph based on selected role
    console.log('Updating visualization for role:', role);
    // In production, this would make an API call and update the visualization
}

// Panel collapse functionality
const panelCollapse = document.querySelector('.panel-collapse');
const insightsPanel = document.querySelector('.insights-panel');

if (panelCollapse) {
    panelCollapse.addEventListener('click', () => {
        insightsPanel.classList.toggle('collapsed');
        if (insightsPanel.classList.contains('collapsed')) {
            insightsPanel.style.width = '60px';
            panelCollapse.querySelector('svg').style.transform = 'rotate(180deg)';
        } else {
            insightsPanel.style.width = '350px';
            panelCollapse.querySelector('svg').style.transform = 'rotate(0deg)';
        }
    });
}

// Animate skill bars on load
function animateSkillBars() {
    const skillBars = document.querySelectorAll('.skill-progress');
    skillBars.forEach((bar, index) => {
        const width = bar.style.width;
        bar.style.width = '0';
        setTimeout(() => {
            bar.style.width = width;
        }, index * 100);
    });
}

// Animate on page load
setTimeout(animateSkillBars, 500);

// Add pulsing effect to high-density regions
function pulseRegions() {
    const highDensityRegions = document.querySelectorAll('.region-marker.high-density');
    highDensityRegions.forEach((region, index) => {
        setInterval(() => {
            region.style.opacity = region.style.opacity === '1' ? '0.7' : '1';
        }, 2000 + (index * 500));
    });
}

pulseRegions();

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Press 'M' for map view
    if (e.key === 'm' || e.key === 'M') {
        document.querySelector('[data-view="map"]').click();
    }
    // Press 'G' for graph view
    if (e.key === 'g' || e.key === 'G') {
        document.querySelector('[data-view="graph"]').click();
    }
    // Press 'Escape' to close cards
    if (e.key === 'Escape') {
        document.getElementById('region-card').style.display = 'none';
        document.getElementById('skill-card').style.display = 'none';
    }
});

// Add tooltip functionality
function initTooltips() {
    const elements = document.querySelectorAll('[title]');
    elements.forEach(el => {
        el.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'custom-tooltip';
            tooltip.textContent = this.getAttribute('title');
            tooltip.style.position = 'absolute';
            tooltip.style.background = 'rgba(26, 26, 26, 0.95)';
            tooltip.style.border = '1px solid var(--accent-green)';
            tooltip.style.padding = '0.5rem 1rem';
            tooltip.style.fontSize = '0.85rem';
            tooltip.style.pointerEvents = 'none';
            tooltip.style.zIndex = '1000';
            tooltip.style.left = e.pageX + 'px';
            tooltip.style.top = (e.pageY - 40) + 'px';
            document.body.appendChild(tooltip);
            
            this.addEventListener('mouseleave', () => {
                tooltip.remove();
            });
        });
    });
}

initTooltips();
