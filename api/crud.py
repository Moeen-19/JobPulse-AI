from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, asc, and_, or_, extract, cast, Date
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta

from . import models, schemas

def get_jobs(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    title: Optional[str] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
    remote: Optional[bool] = None,
    min_salary: Optional[float] = None,
    max_salary: Optional[float] = None,
    skills: Optional[List[str]] = None,
    date_filter: Optional[date] = None,
    sort_by: str = "posted_date",
    sort_order: str = "desc"
) -> List[models.Job]:
    """
    Get jobs with filtering and sorting options
    """
    query = db.query(models.Job).join(models.Company).join(models.Location, isouter=True)
    
    # Apply filters
    if title:
        query = query.filter(models.Job.title.ilike(f"%{title}%"))
    
    if company:
        query = query.filter(models.Company.name.ilike(f"%{company}%"))
    
    if location:
        query = query.filter(or_(
            models.Location.city.ilike(f"%{location}%"),
            models.Location.state.ilike(f"%{location}%"),
            models.Location.country.ilike(f"%{location}%")
        ))
    
    if remote is not None:
        query = query.filter(models.Location.is_remote == remote)
    
    if min_salary is not None:
        query = query.filter(models.Job.salary_min >= min_salary)
    
    if max_salary is not None:
        query = query.filter(models.Job.salary_max <= max_salary)
    
    if skills:
        for skill in skills:
            skill_subquery = db.query(models.Skill.id).filter(models.Skill.name.ilike(f"%{skill}%")).subquery()
            query = query.join(
                models.job_skills,
                models.Job.id == models.job_skills.c.job_id
            ).filter(models.job_skills.c.skill_id.in_(skill_subquery))
    
    if date_filter:
        query = query.filter(models.Job.posted_date >= date_filter)
    
    # Apply sorting
    if sort_by == "posted_date":
        if sort_order.lower() == "asc":
            query = query.order_by(asc(models.Job.posted_date))
        else:
            query = query.order_by(desc(models.Job.posted_date))
    elif sort_by == "salary":
        # Sort by average of min and max salary
        if sort_order.lower() == "asc":
            query = query.order_by(asc((models.Job.salary_min + models.Job.salary_max) / 2))
        else:
            query = query.order_by(desc((models.Job.salary_min + models.Job.salary_max) / 2))
    elif sort_by == "title":
        if sort_order.lower() == "asc":
            query = query.order_by(asc(models.Job.title))
        else:
            query = query.order_by(desc(models.Job.title))
    elif sort_by == "company":
        if sort_order.lower() == "asc":
            query = query.order_by(asc(models.Company.name))
        else:
            query = query.order_by(desc(models.Company.name))
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    # Eager load relationships
    query = query.options(
        joinedload(models.Job.company),
        joinedload(models.Job.location)
    )
    
    return query.all()

def get_job(db: Session, job_id: int) -> Optional[models.Job]:
    """
    Get a specific job by ID with all related data
    """
    return db.query(models.Job).options(
        joinedload(models.Job.company),
        joinedload(models.Job.location),
        joinedload(models.Job.skills)
    ).filter(models.Job.id == job_id).first()

def get_companies(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    name: Optional[str] = None
) -> List[models.Company]:
    """
    Get companies with optional name filter
    """
    query = db.query(models.Company)
    
    if name:
        query = query.filter(models.Company.name.ilike(f"%{name}%"))
    
    return query.offset(skip).limit(limit).all()

def get_company(db: Session, company_id: int) -> Optional[models.Company]:
    """
    Get a specific company by ID
    """
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    
    if company:
        # Get job count for this company
        job_count = db.query(func.count(models.Job.id)).filter(
            models.Job.company_id == company_id
        ).scalar()
        
        # Attach job count to company object
        setattr(company, "job_count", job_count)
    
    return company

def get_company_jobs(
    db: Session, 
    company_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[models.Job]:
    """
    Get jobs for a specific company
    """
    return db.query(models.Job).options(
        joinedload(models.Job.company),
        joinedload(models.Job.location)
    ).filter(
        models.Job.company_id == company_id
    ).order_by(
        desc(models.Job.posted_date)
    ).offset(skip).limit(limit).all()

def get_locations(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    city: Optional[str] = None,
    state: Optional[str] = None,
    country: Optional[str] = None,
    remote: Optional[bool] = None
) -> List[models.Location]:
    """
    Get locations with optional filters
    """
    query = db.query(models.Location)
    
    if city:
        query = query.filter(models.Location.city.ilike(f"%{city}%"))
    
    if state:
        query = query.filter(models.Location.state.ilike(f"%{state}%"))
    
    if country:
        query = query.filter(models.Location.country.ilike(f"%{country}%"))
    
    if remote is not None:
        query = query.filter(models.Location.is_remote == remote)
    
    return query.offset(skip).limit(limit).all()

def get_location(db: Session, location_id: int) -> Optional[models.Location]:
    """
    Get a specific location by ID
    """
    return db.query(models.Location).filter(models.Location.id == location_id).first()

def get_location_jobs(
    db: Session, 
    location_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[models.Job]:
    """
    Get jobs for a specific location
    """
    return db.query(models.Job).options(
        joinedload(models.Job.company),
        joinedload(models.Job.location)
    ).filter(
        models.Job.location_id == location_id
    ).order_by(
        desc(models.Job.posted_date)
    ).offset(skip).limit(limit).all()

def get_skills(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    name: Optional[str] = None,
    category: Optional[str] = None
) -> List[models.Skill]:
    """
    Get skills with optional filters
    """
    query = db.query(models.Skill)
    
    if name:
        query = query.filter(models.Skill.name.ilike(f"%{name}%"))
    
    if category:
        query = query.filter(models.Skill.category.ilike(f"%{category}%"))
    
    return query.offset(skip).limit(limit).all()

def get_skill(db: Session, skill_id: int) -> Optional[models.Skill]:
    """
    Get a specific skill by ID with job count and average salary
    """
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    
    if skill:
        # Get job count for this skill
        job_count = db.query(func.count(models.job_skills.c.job_id)).filter(
            models.job_skills.c.skill_id == skill_id
        ).scalar()
        
        # Get average salary for jobs with this skill
        avg_salary_query = db.query(
            func.avg((models.Job.salary_min + models.Job.salary_max) / 2)
        ).join(
            models.job_skills,
            models.Job.id == models.job_skills.c.job_id
        ).filter(
            models.job_skills.c.skill_id == skill_id,
            models.Job.salary_min.isnot(None),
            models.Job.salary_max.isnot(None)
        ).scalar()
        
        # Attach additional data to skill object
        setattr(skill, "job_count", job_count)
        setattr(skill, "avg_salary", avg_salary_query)
    
    return skill

def get_skill_jobs(
    db: Session, 
    skill_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[models.Job]:
    """
    Get jobs requiring a specific skill
    """
    return db.query(models.Job).options(
        joinedload(models.Job.company),
        joinedload(models.Job.location)
    ).join(
        models.job_skills,
        models.Job.id == models.job_skills.c.job_id
    ).filter(
        models.job_skills.c.skill_id == skill_id
    ).order_by(
        desc(models.Job.posted_date)
    ).offset(skip).limit(limit).all()

def get_trending_skills(
    db: Session,
    date_filter: date,
    limit: int = 20,
    category: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get trending skills based on job postings
    """
    # Get current trending data
    current_query = db.query(
        models.Skill,
        models.TrendingInsight.job_count,
        models.TrendingInsight.avg_salary
    ).join(
        models.TrendingInsight,
        models.Skill.id == models.TrendingInsight.skill_id
    ).filter(
        models.TrendingInsight.date == date.today()
    )
    
    # Apply category filter if provided
    if category:
        current_query = current_query.filter(models.Skill.category == category)
    
    # Get previous period data for comparison (30 days ago)
    previous_date = date.today() - timedelta(days=30)
    
    # Create a subquery for previous period data
    previous_subquery = db.query(
        models.TrendingInsight.skill_id,
        models.TrendingInsight.job_count.label('previous_count')
    ).filter(
        models.TrendingInsight.date == previous_date
    ).subquery()
    
    # Join with previous period data
    current_query = current_query.outerjoin(
        previous_subquery,
        models.Skill.id == previous_subquery.c.skill_id
    )
    
    # Select additional column for growth rate
    current_query = current_query.add_columns(
        (
            (models.TrendingInsight.job_count - func.coalesce(previous_subquery.c.previous_count, 0)) / 
            func.nullif(func.coalesce(previous_subquery.c.previous_count, 0), 0) * 100
        ).label('growth_rate')
    )
    
    # Order by job count (most in-demand skills)
    current_query = current_query.order_by(desc(models.TrendingInsight.job_count))
    
    # Apply limit
    current_query = current_query.limit(limit)
    
    # Execute query
    results = current_query.all()
    
    # Format results
    trending_skills = []
    for skill, job_count, avg_salary, growth_rate in results:
        trending_skills.append({
            "skill": skill,
            "job_count": job_count,
            "avg_salary": avg_salary,
            "growth_rate": growth_rate
        })
    
    return trending_skills

def get_salary_insights(
    db: Session,
    date_filter: date,
    skill: Optional[str] = None,
    location: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get salary insights for different job categories
    """
    # Base query for salary data grouped by job title
    query = db.query(
        models.Job.title,
        func.avg((models.Job.salary_min + models.Job.salary_max) / 2).label('avg_salary'),
        func.min(models.Job.salary_min).label('min_salary'),
        func.max(models.Job.salary_max).label('max_salary'),
        func.mode().within_group(models.Job.salary_currency).label('currency'),
        func.mode().within_group(models.Job.salary_period).label('period'),
        func.count(models.Job.id).label('job_count')
    ).filter(
        models.Job.posted_date >= date_filter,
        models.Job.salary_min.isnot(None),
        models.Job.salary_max.isnot(None)
    )
    
    # Apply skill filter if provided
    if skill:
        skill_subquery = db.query(models.Skill.id).filter(
            models.Skill.name.ilike(f"%{skill}%")
        ).subquery()
        
        query = query.join(
            models.job_skills,
            models.Job.id == models.job_skills.c.job_id
        ).filter(
            models.job_skills.c.skill_id.in_(skill_subquery)
        )
    
    # Apply location filter if provided
    if location:
        query = query.join(models.Location).filter(
            or_(
                models.Location.city.ilike(f"%{location}%"),
                models.Location.state.ilike(f"%{location}%"),
                models.Location.country.ilike(f"%{location}%")
            )
        )
    
    # Group by job title
    query = query.group_by(models.Job.title)
    
    # Order by job count (most common jobs first)
    query = query.order_by(desc('job_count'))
    
    # Execute query
    results = query.all()
    
    # Format results
    salary_insights = []
    for title, avg_salary, min_salary, max_salary, currency, period, job_count in results:
        salary_insights.append({
            "title": title,
            "avg_salary": avg_salary,
            "min_salary": min_salary,
            "max_salary": max_salary,
            "currency": currency or "USD",
            "period": period or "year",
            "job_count": job_count
        })
    
    return salary_insights

def get_job_growth(
    db: Session,
    date_filter: date,
    interval: str = "week",
    skill: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get job posting growth over time
    """
    # Determine date trunc function based on interval
    if interval == "day":
        date_trunc = func.date_trunc('day', models.Job.posted_date)
    elif interval == "week":
        date_trunc = func.date_trunc('week', models.Job.posted_date)
    elif interval == "month":
        date_trunc = func.date_trunc('month', models.Job.posted_date)
    else:
        date_trunc = func.date_trunc('week', models.Job.posted_date)
    
    # Base query for job count by date
    query = db.query(
        cast(date_trunc, Date).label('date'),
        func.count(models.Job.id).label('count')
    ).filter(
        models.Job.posted_date >= date_filter
    )
    
    # Apply skill filter if provided
    if skill:
        skill_subquery = db.query(models.Skill.id).filter(
            models.Skill.name.ilike(f"%{skill}%")
        ).subquery()
        
        query = query.join(
            models.job_skills,
            models.Job.id == models.job_skills.c.job_id
        ).filter(
            models.job_skills.c.skill_id.in_(skill_subquery)
        )
    
    # Group by date
    query = query.group_by('date')
    
    # Order by date
    query = query.order_by(asc('date'))
    
    # Execute query
    results = query.all()
    
    # Format results
    growth_data = {
        "skill": skill,
        "data_points": [
            {"date": date_val, "count": count} for date_val, count in results
        ]
    }
    
    return [growth_data]

def search(
    db: Session,
    query: str,
    limit: int = 10
) -> Dict[str, List]:
    """
    Search across jobs, companies, and skills
    """
    # Search jobs
    jobs = db.query(models.Job).options(
        joinedload(models.Job.company),
        joinedload(models.Job.location)
    ).filter(
        or_(
            models.Job.title.ilike(f"%{query}%"),
            models.Job.description.ilike(f"%{query}%")
        )
    ).order_by(desc(models.Job.posted_date)).limit(limit).all()
    
    # Search companies
    companies = db.query(models.Company).filter(
        or_(
            models.Company.name.ilike(f"%{query}%"),
            models.Company.description.ilike(f"%{query}%")
        )
    ).limit(limit).all()
    
    # Search skills
    skills = db.query(models.Skill).filter(
        models.Skill.name.ilike(f"%{query}%")
    ).limit(limit).all()
    
    return {
        "jobs": jobs,
        "companies": companies,
        "skills": skills
    }