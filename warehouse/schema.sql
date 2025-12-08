-- JobPulse Database Schema

-- Companies table
CREATE TABLE IF NOT EXISTS companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on company name
CREATE INDEX IF NOT EXISTS idx_companies_name ON companies(company_name);

-- Locations table
CREATE TABLE IF NOT EXISTS locations (
    location_id SERIAL PRIMARY KEY,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    is_remote BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on location components
CREATE INDEX IF NOT EXISTS idx_locations_components ON locations(city, state, country);

-- Skills table
CREATE TABLE IF NOT EXISTS skills (
    skill_id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on skill name
CREATE INDEX IF NOT EXISTS idx_skills_name ON skills(skill_name);

-- Jobs table
CREATE TABLE IF NOT EXISTS jobs (
    job_id SERIAL PRIMARY KEY,
    external_job_id VARCHAR(100),
    title VARCHAR(255) NOT NULL,
    company_id INTEGER REFERENCES companies(company_id),
    location_id INTEGER REFERENCES locations(location_id),
    description TEXT,
    salary_min NUMERIC,
    salary_max NUMERIC,
    salary_currency VARCHAR(10),
    salary_period VARCHAR(20),
    job_type VARCHAR(50),
    url VARCHAR(500),
    source VARCHAR(50) NOT NULL,
    posted_date TIMESTAMP,
    scraped_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for jobs table
CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title);
CREATE INDEX IF NOT EXISTS idx_jobs_company_id ON jobs(company_id);
CREATE INDEX IF NOT EXISTS idx_jobs_location_id ON jobs(location_id);
CREATE INDEX IF NOT EXISTS idx_jobs_source ON jobs(source);
CREATE INDEX IF NOT EXISTS idx_jobs_posted_date ON jobs(posted_date);
CREATE INDEX IF NOT EXISTS idx_jobs_external_id ON jobs(external_job_id);

-- Job Skills mapping table (many-to-many)
CREATE TABLE IF NOT EXISTS job_skills (
    job_id INTEGER REFERENCES jobs(job_id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(skill_id) ON DELETE CASCADE,
    PRIMARY KEY (job_id, skill_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on job_skills
CREATE INDEX IF NOT EXISTS idx_job_skills_skill_id ON job_skills(skill_id);

-- Trending insights table (for pre-computed analytics)
CREATE TABLE IF NOT EXISTS trending_insights (
    insight_id SERIAL PRIMARY KEY,
    skill_id INTEGER REFERENCES skills(skill_id),
    job_count INTEGER NOT NULL,
    growth_rate NUMERIC,
    time_period VARCHAR(20) NOT NULL,
    location_id INTEGER REFERENCES locations(location_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for trending insights
CREATE INDEX IF NOT EXISTS idx_trending_insights_skill ON trending_insights(skill_id);
CREATE INDEX IF NOT EXISTS idx_trending_insights_location ON trending_insights(location_id);

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers to automatically update the updated_at column
CREATE TRIGGER update_companies_modtime
BEFORE UPDATE ON companies
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_locations_modtime
BEFORE UPDATE ON locations
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_skills_modtime
BEFORE UPDATE ON skills
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_jobs_modtime
BEFORE UPDATE ON jobs
FOR EACH ROW EXECUTE FUNCTION update_modified_column();