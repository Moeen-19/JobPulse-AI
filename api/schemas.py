from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import date, datetime

class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None

class Skill(SkillBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class SkillDetail(Skill):
    job_count: int = 0
    avg_salary: Optional[float] = None
    
    model_config = ConfigDict(from_attributes=True)

class LocationBase(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    is_remote: bool = False

class Location(LocationBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class CompanyBase(BaseModel):
    name: str
    website: Optional[str] = None
    description: Optional[str] = None

class Company(CompanyBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class CompanyDetail(Company):
    job_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)

class JobBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: Optional[str] = None
    salary_period: Optional[str] = None
    posted_date: Optional[date] = None
    source: Optional[str] = None

class Job(JobBase):
    id: int
    company: Company
    location: Optional[Location] = None
    
    model_config = ConfigDict(from_attributes=True)

class JobDetail(Job):
    skills: List[Skill] = []
    
    model_config = ConfigDict(from_attributes=True)

class TrendingSkill(BaseModel):
    skill: Skill
    job_count: int
    avg_salary: Optional[float] = None
    growth_rate: Optional[float] = None  # Percentage growth over the period
    
    model_config = ConfigDict(from_attributes=True)

class SalaryInsight(BaseModel):
    title: str
    avg_salary: float
    min_salary: float
    max_salary: float
    currency: str = "USD"
    period: str = "year"
    job_count: int
    
    model_config = ConfigDict(from_attributes=True)

class JobGrowthPoint(BaseModel):
    date: date
    count: int

class JobGrowthInsight(BaseModel):
    skill: Optional[str] = None
    data_points: List[JobGrowthPoint]
    
    model_config = ConfigDict(from_attributes=True)

class SearchResult(BaseModel):
    type: str  # "job", "company", "skill"
    id: int
    title: str
    description: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class SearchResults(BaseModel):
    jobs: List[Job] = []
    companies: List[Company] = []
    skills: List[Skill] = []
    
    model_config = ConfigDict(from_attributes=True)
