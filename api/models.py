from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, Text, Float, DateTime,
    Table, Index, Numeric
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

# --- Association Table (job_skills) ---
job_skills = Table(
    "job_skills",
    Base.metadata,
    Column("job_id", Integer, ForeignKey("jobs.job_id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.skill_id", ondelete="CASCADE"), primary_key=True),
)


# --- Companies Table ---
class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False, unique=True, index=True)
    industry = Column(String(100))
    website = Column(String(255))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships
    jobs = relationship("Job", back_populates="company")

    def __repr__(self):
        return f"<Company(name='{self.company_name}')>"


# --- Locations Table ---
class Location(Base):
    __tablename__ = "locations"

    location_id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    is_remote = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships
    jobs = relationship("Job", back_populates="location")

    __table_args__ = (
        Index("idx_locations_components", "city", "state", "country"),
    )

    def __repr__(self):
        return f"<Location(city='{self.city}', country='{self.country}')>"


# --- Skills Table ---
class Skill(Base):
    __tablename__ = "skills"

    skill_id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(100), nullable=False, unique=True, index=True)
    category = Column(String(50))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships
    jobs = relationship("Job", secondary=job_skills, back_populates="skills")
    trending_insights = relationship("TrendingInsight", back_populates="skill")

    def __repr__(self):
        return f"<Skill(name='{self.skill_name}', category='{self.category}')>"


# --- Jobs Table ---
class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(Integer, primary_key=True, index=True)
    external_job_id = Column(String(100))
    title = Column(String(255), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.location_id"))
    description = Column(Text)
    salary_min = Column(Numeric)
    salary_max = Column(Numeric)
    salary_currency = Column(String(10))
    salary_period = Column(String(20))
    job_type = Column(String(50))
    url = Column(String(500), unique=True)
    source = Column(String(50), nullable=False)
    posted_date = Column(DateTime)
    scraped_date = Column(DateTime, default=datetime.now(timezone.utc))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships
    company = relationship("Company", back_populates="jobs")
    location = relationship("Location", back_populates="jobs")
    skills = relationship("Skill", secondary=job_skills, back_populates="jobs")

    __table_args__ = (
        Index("idx_jobs_title", "title"),
        Index("idx_jobs_company_id", "company_id"),
        Index("idx_jobs_location_id", "location_id"),
        Index("idx_jobs_source", "source"),
        Index("idx_jobs_posted_date", "posted_date"),
        Index("idx_jobs_external_id", "external_job_id"),
    )

    def __repr__(self):
        return f"<Job(title='{self.title}', company_id={self.company_id})>"


# --- Trending Insights Table ---
class TrendingInsight(Base):
    __tablename__ = "trending_insights"

    insight_id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), nullable=False)
    job_count = Column(Integer, nullable=False, default=0)
    growth_rate = Column(Float)
    time_period = Column(String(20), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.location_id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships
    skill = relationship("Skill", back_populates="trending_insights")
    location = relationship("Location")

    __table_args__ = (
        Index("idx_trending_insights_skill", "skill_id"),
        Index("idx_trending_insights_location", "location_id"),
    )

    def __repr__(self):
        return f"<TrendingInsight(skill_id={self.skill_id}, job_count={self.job_count})>"
