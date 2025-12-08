from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, timedelta
from api.database import get_db, engine
from api import models, schemas, crud
# ML imports moved to endpoint functions to avoid circular imports
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JobPulse API",
    description="API for accessing job market data and insights",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific front-end domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to JobPulse API",
        "version": "1.0.0",
        "docs": "/docs",
    }

@app.get("/jobs", response_model=List[schemas.Job], tags=["Jobs"])
async def get_jobs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
    remote: Optional[bool] = None,
    min_salary: Optional[float] = None,
    max_salary: Optional[float] = None,
    skills: Optional[List[str]] = Query(None),
    days: Optional[int] = None,
    sort_by: Optional[str] = "posted_date",
    sort_order: Optional[str] = "desc",
):
    """
    Get jobs with optional filtering and sorting
    """
    # Calculate date filter if days is provided
    date_filter = None
    if days:
        date_filter = date.today() - timedelta(days=days)
    
    jobs = crud.get_jobs(
        db, 
        skip=skip, 
        limit=limit,
        title=title,
        company=company,
        location=location,
        remote=remote,
        min_salary=min_salary,
        max_salary=max_salary,
        skills=skills,
        date_filter=date_filter,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return jobs

@app.get("/jobs/{job_id}", response_model=schemas.JobDetail, tags=["Jobs"])
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific job
    """
    job = crud.get_job(db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/companies", response_model=List[schemas.Company], tags=["Companies"])
async def get_companies(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
):
    """
    Get list of companies with optional filtering
    """
    companies = crud.get_companies(db, skip=skip, limit=limit, name=name)
    return companies

@app.get("/companies/{company_id}", response_model=schemas.CompanyDetail, tags=["Companies"])
async def get_company(company_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific company
    """
    company = crud.get_company(db, company_id=company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.get("/companies/{company_id}/jobs", response_model=List[schemas.Job], tags=["Companies"])
async def get_company_jobs(
    company_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get jobs posted by a specific company
    """
    company = crud.get_company(db, company_id=company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    
    jobs = crud.get_company_jobs(db, company_id=company_id, skip=skip, limit=limit)
    return jobs

@app.get("/locations", response_model=List[schemas.Location], tags=["Locations"])
async def get_locations(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    city: Optional[str] = None,
    state: Optional[str] = None,
    country: Optional[str] = None,
    remote: Optional[bool] = None,
):
    """
    Get list of locations with optional filtering
    """
    locations = crud.get_locations(
        db, 
        skip=skip, 
        limit=limit,
        city=city,
        state=state,
        country=country,
        remote=remote
    )
    return locations

@app.get("/locations/{location_id}/jobs", response_model=List[schemas.Job], tags=["Locations"])
async def get_location_jobs(
    location_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get jobs in a specific location
    """
    location = crud.get_location(db, location_id=location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    
    jobs = crud.get_location_jobs(db, location_id=location_id, skip=skip, limit=limit)
    return jobs

@app.get("/skills", response_model=List[schemas.Skill], tags=["Skills"])
async def get_skills(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    category: Optional[str] = None,
):
    """
    Get list of skills with optional filtering
    """
    skills = crud.get_skills(
        db, 
        skip=skip, 
        limit=limit,
        name=name,
        category=category
    )
    return skills

@app.get("/skills/{skill_id}", response_model=schemas.SkillDetail, tags=["Skills"])
async def get_skill(skill_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific skill
    """
    skill = crud.get_skill(db, skill_id=skill_id)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@app.get("/skills/{skill_id}/jobs", response_model=List[schemas.Job], tags=["Skills"])
async def get_skill_jobs(
    skill_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get jobs requiring a specific skill
    """
    skill = crud.get_skill(db, skill_id=skill_id)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    jobs = crud.get_skill_jobs(db, skill_id=skill_id, skip=skip, limit=limit)
    return jobs

@app.get("/insights/trending-skills", response_model=List[schemas.TrendingSkill], tags=["Insights"])
async def get_trending_skills(
    db: Session = Depends(get_db),
    days: int = 30,
    limit: int = 20,
    category: Optional[str] = None,
):
    """
    Get trending skills based on job postings
    """
    date_filter = date.today() - timedelta(days=days)
    
    trending_skills = crud.get_trending_skills(
        db,
        date_filter=date_filter,
        limit=limit,
        category=category
    )
    return trending_skills

@app.get("/insights/salary-ranges", response_model=List[schemas.SalaryInsight], tags=["Insights"])
async def get_salary_ranges(
    db: Session = Depends(get_db),
    skill: Optional[str] = None,
    location: Optional[str] = None,
    days: int = 90,
):
    """
    Get salary ranges for different job categories
    """
    date_filter = date.today() - timedelta(days=days)
    
    salary_insights = crud.get_salary_insights(
        db,
        date_filter=date_filter,
        skill=skill,
        location=location
    )
    return salary_insights

@app.get("/insights/job-growth", response_model=List[schemas.JobGrowthInsight], tags=["Insights"])
async def get_job_growth(
    db: Session = Depends(get_db),
    days: int = 90,
    interval: str = "week",
    skill: Optional[str] = None,
):
    """
    Get job posting growth over time
    """
    date_filter = date.today() - timedelta(days=days)
    
    growth_insights = crud.get_job_growth(
        db,
        date_filter=date_filter,
        interval=interval,
        skill=skill
    )
    return growth_insights

@app.get("/ml/skill-forecast", tags=["ML Insights"])
async def skill_forecast(skill: str, region: Optional[str] = None, days_ahead: int = 30, db: Session = Depends(get_db)):
    """Get skill demand forecast using Prophet ML model"""
    from api.ml.forecasting import run_forecast
    return run_forecast(db, skill, region, days_ahead)

@app.get("/ml/skill-correlations", tags=["ML Insights"])
async def skill_correlations(region: Optional[str] = None, top_n: int = 20, db: Session = Depends(get_db)):
    """Get skill correlation analysis based on co-occurrence in job postings"""
    from api.ml.correlation import run_correlation
    return run_correlation(db, region, top_n)

@app.get("/search", response_model=schemas.SearchResults, tags=["Search"])
async def search(
    q: str,
    db: Session = Depends(get_db),
    limit: int = 10,
):
    """
    Search across jobs, companies, and skills
    """
    results = crud.search(db, query=q, limit=limit)
    return results

if __name__ == "__main__":
    import uvicorn
    import os
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("api.main:app", host=host, port=port, reload=False)
