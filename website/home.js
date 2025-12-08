// Home Page - Real API Integration

document.addEventListener('DOMContentLoaded', async () => {
    await loadHomePageData();
});

async function loadHomePageData() {
    try {
        // Show loading state
        showLoadingState();

        // Load data in parallel
        const [jobs, trendingSkills, companies] = await Promise.all([
            api.getJobs({ limit: 10, days: 30 }).catch(err => ({ error: err.message })),
            api.getTrendingSkills(30, 10).catch(err => ({ error: err.message })),
            api.getCompanies({ limit: 10 }).catch(err => ({ error: err.message }))
        ]);

        // Update stats with real data
        updateStats(jobs, trendingSkills, companies);

        // Update trending skills section
        updateTrendingSkills(trendingSkills);

        // Update companies hiring section
        updateCompaniesHiring(companies);

        // Hide loading state
        hideLoadingState();

    } catch (error) {
        console.error('Error loading home page data:', error);
        showErrorState('Unable to load data. Please ensure the API server is running on http://localhost:8000');
    }
}

function updateStats(jobs, trendingSkills, companies) {
    // Update job count
    const jobCountElement = document.querySelector('.stat-card:nth-child(1) .stat-number');
    if (jobCountElement && Array.isArray(jobs)) {
        jobCountElement.textContent = `${jobs.length}+ Jobs`;
    }

    // Update recruiters count (companies)
    const recruitersElement = document.querySelector('.stat-card:nth-child(2) .stat-number');
    if (recruitersElement && Array.isArray(companies)) {
        recruitersElement.textContent = `${companies.length}+ Recruiters`;
    }

    // Update trending skills count
    const skillsElement = document.querySelector('.stat-card:nth-child(3) .stat-number');
    if (skillsElement && Array.isArray(trendingSkills)) {
        skillsElement.textContent = `${trendingSkills.length}+ Skills`;
    }
}

function updateTrendingSkills(trendingSkills) {
    if (!Array.isArray(trendingSkills) || trendingSkills.length === 0) {
        console.log('No trending skills data available');
        return;
    }

    // Update the skills list in the insights section
    const skillListContainer = document.querySelector('.insight-content .trending-list');
    if (skillListContainer) {
        skillListContainer.innerHTML = '';
        
        // Show top 3 skills
        trendingSkills.slice(0, 3).forEach(skillData => {
            const li = document.createElement('li');
            li.textContent = skillData.skill?.skill_name || skillData.skill?.name || 'Unknown';
            li.style.color = 'var(--accent-green)';
            skillListContainer.appendChild(li);
        });
    }
}

function updateCompaniesHiring(companies) {
    if (!Array.isArray(companies) || companies.length === 0) {
        console.log('No companies data available');
        return;
    }

    // Update companies list in the insights panel
    const companyListContainer = document.querySelector('.company-list');
    if (companyListContainer) {
        companyListContainer.innerHTML = '';
        
        // Show top 3 companies
        companies.slice(0, 3).forEach(company => {
            const companyItem = document.createElement('div');
            companyItem.className = 'company-item';
            
            const companyName = company.company_name || company.name || 'Unknown Company';
            const initial = companyName.charAt(0).toUpperCase();
            
            companyItem.innerHTML = `
                <div class="company-logo">${initial}</div>
                <div class="company-info">
                    <span class="company-name">${companyName}</span>
                    <span class="company-jobs">${company.job_count || 'Multiple'} positions</span>
                </div>
            `;
            
            companyListContainer.appendChild(companyItem);
        });
    }
}

function showLoadingState() {
    const statsCards = document.querySelectorAll('.stat-card');
    statsCards.forEach(card => {
        card.style.opacity = '0.5';
    });
}

function hideLoadingState() {
    const statsCards = document.querySelectorAll('.stat-card');
    statsCards.forEach(card => {
        card.style.opacity = '1';
    });
}

function showErrorState(message) {
    // Create error notification
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background: #ff6b6b;
        color: white;
        padding: 1rem 2rem;
        border-radius: 4px;
        z-index: 1000;
        max-width: 400px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    `;
    errorDiv.innerHTML = `
        <strong>⚠️ Connection Error</strong><br>
        <small>${message}</small>
    `;
    
    document.body.appendChild(errorDiv);
    
    // Auto-remove after 10 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 10000);
}

// Add API status indicator
async function checkAPIStatus() {
    try {
        await api.healthCheck();
        console.log('✅ API connection successful');
        return true;
    } catch (error) {
        console.error('❌ API connection failed:', error);
        showErrorState('API server is not responding. Please start the FastAPI server: uvicorn api.main:app --reload');
        return false;
    }
}

// Check API status on page load
checkAPIStatus();
