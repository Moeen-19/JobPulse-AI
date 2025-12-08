// API Client for JobPulse Frontend
// Handles all communication with FastAPI backend

class JobPulseAPI {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }

    // Helper method for making requests
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            throw error;
        }
    }

    // Jobs endpoints
    async getJobs(filters = {}) {
        const params = new URLSearchParams();
        
        Object.keys(filters).forEach(key => {
            if (filters[key] !== null && filters[key] !== undefined && filters[key] !== '') {
                if (Array.isArray(filters[key])) {
                    filters[key].forEach(val => params.append(key, val));
                } else {
                    params.append(key, filters[key]);
                }
            }
        });

        const queryString = params.toString();
        const endpoint = queryString ? `/jobs?${queryString}` : '/jobs';
        
        return this.request(endpoint);
    }

    async getJob(jobId) {
        return this.request(`/jobs/${jobId}`);
    }

    async searchJobs(query, limit = 10) {
        return this.request(`/search?q=${encodeURIComponent(query)}&limit=${limit}`);
    }

    // Skills endpoints
    async getSkills(filters = {}) {
        const params = new URLSearchParams(filters);
        const queryString = params.toString();
        const endpoint = queryString ? `/skills?${queryString}` : '/skills';
        
        return this.request(endpoint);
    }

    async getSkill(skillId) {
        return this.request(`/skills/${skillId}`);
    }

    async getSkillJobs(skillId, skip = 0, limit = 100) {
        return this.request(`/skills/${skillId}/jobs?skip=${skip}&limit=${limit}`);
    }

    // Companies endpoints
    async getCompanies(filters = {}) {
        const params = new URLSearchParams(filters);
        const queryString = params.toString();
        const endpoint = queryString ? `/companies?${queryString}` : '/companies';
        
        return this.request(endpoint);
    }

    async getCompany(companyId) {
        return this.request(`/companies/${companyId}`);
    }

    async getCompanyJobs(companyId, skip = 0, limit = 100) {
        return this.request(`/companies/${companyId}/jobs?skip=${skip}&limit=${limit}`);
    }

    // Locations endpoints
    async getLocations(filters = {}) {
        const params = new URLSearchParams(filters);
        const queryString = params.toString();
        const endpoint = queryString ? `/locations?${queryString}` : '/locations';
        
        return this.request(endpoint);
    }

    async getLocationJobs(locationId, skip = 0, limit = 100) {
        return this.request(`/locations/${locationId}/jobs?skip=${skip}&limit=${limit}`);
    }

    // Analytics endpoints
    async getTrendingSkills(days = 30, limit = 20, category = null) {
        const params = new URLSearchParams({ days, limit });
        if (category) params.append('category', category);
        
        return this.request(`/insights/trending-skills?${params.toString()}`);
    }

    async getSalaryInsights(days = 90, skill = null, location = null) {
        const params = new URLSearchParams({ days });
        if (skill) params.append('skill', skill);
        if (location) params.append('location', location);
        
        return this.request(`/insights/salary-ranges?${params.toString()}`);
    }

    async getJobGrowth(days = 90, interval = 'week', skill = null) {
        const params = new URLSearchParams({ days, interval });
        if (skill) params.append('skill', skill);
        
        return this.request(`/insights/job-growth?${params.toString()}`);
    }

    // ML endpoints
    async getSkillForecast(skill, region = null, daysAhead = 180) {
        const params = new URLSearchParams({ skill, days_ahead: daysAhead });
        if (region) params.append('region', region);
        
        return this.request(`/ml/skill-forecast?${params.toString()}`);
    }

    async getSkillCorrelations(region = null, topN = 20) {
        const params = new URLSearchParams({ top_n: topN });
        if (region) params.append('region', region);
        
        return this.request(`/ml/skill-correlations?${params.toString()}`);
    }

    // Health check
    async healthCheck() {
        return this.request('/');
    }
}

// Create singleton instance
const api = new JobPulseAPI();

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
}
