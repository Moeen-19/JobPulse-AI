#!/usr/bin/env python3
"""
Generate sample data for testing JobPulse without running scrapers
This populates the database with realistic test data
"""

import os
import sys
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from api.database import SessionLocal, engine
from api import models

# Sample data
COMPANIES = [
    "Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix", "Tesla",
    "Uber", "Airbnb", "Stripe", "Shopify", "Spotify", "Twitter", "LinkedIn"
]

LOCATIONS = [
    {"city": "San Francisco", "state": "CA", "country": "United States", "is_remote": False},
    {"city": "New York", "state": "NY", "country": "United States", "is_remote": False},
    {"city": "Seattle", "state": "WA", "country": "United States", "is_remote": False},
    {"city": "Austin", "state": "TX", "country": "United States", "is_remote": False},
    {"city": "London", "state": None, "country": "United Kingdom", "is_remote": False},
    {"city": "Berlin", "state": None, "country": "Germany", "is_remote": False},
    {"city": "Toronto", "state": "ON", "country": "Canada", "is_remote": False},
    {"city": None, "state": None, "country": None, "is_remote": True},
]

SKILLS = {
    "languages": ["Python", "JavaScript", "TypeScript", "Java", "Go", "Rust", "C++"],
    "frameworks": ["React", "Angular", "Vue", "Django", "Flask", "FastAPI", "Node.js", "Express"],
    "databases": ["PostgreSQL", "MongoDB", "MySQL", "Redis", "Elasticsearch"],
    "cloud": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform"],
    "tools": ["Git", "Linux", "CI/CD", "Agile", "REST API"]
}

JOB_TITLES = [
    "Senior Software Engineer",
    "Full Stack Developer",
    "Backend Engineer",
    "Frontend Developer",
    "Data Scientist",
    "Machine Learning Engineer",
    "DevOps Engineer",
    "Cloud Architect",
    "Product Manager",
    "Engineering Manager"
]

def create_sample_data(num_jobs=100):
    """Generate sample data"""
    db = SessionLocal()
    
    try:
        print("🔧 Creating database tables...")
        models.Base.metadata.create_all(bind=engine)
        
        print("🏢 Creating companies...")
        company_objects = []
        for company_name in COMPANIES:
            company = models.Company(
                company_name=company_name,
                industry="Technology",
                website=f"https://{company_name.lower().replace(' ', '')}.com"
            )
            db.add(company)
            company_objects.append(company)
        db.commit()
        print(f"✅ Created {len(company_objects)} companies")
        
        print("📍 Creating locations...")
        location_objects = []
        for loc_data in LOCATIONS:
            location = models.Location(**loc_data)
            db.add(location)
            location_objects.append(location)
        db.commit()
        print(f"✅ Created {len(location_objects)} locations")
        
        print("🎯 Creating skills...")
        skill_objects = []
        for category, skills in SKILLS.items():
            for skill_name in skills:
                skill = models.Skill(
                    skill_name=skill_name,
                    category=category
                )
                db.add(skill)
                skill_objects.append(skill)
        db.commit()
        print(f"✅ Created {len(skill_objects)} skills")
        
        print(f"💼 Creating {num_jobs} jobs...")
        job_objects = []
        for i in range(num_jobs):
            # Random job details
            company = random.choice(company_objects)
            location = random.choice(location_objects)
            title = random.choice(JOB_TITLES)
            
            # Random date in last 90 days
            days_ago = random.randint(0, 90)
            posted_date = datetime.now() - timedelta(days=days_ago)
            
            # Random salary
            base_salary = random.randint(80, 180) * 1000
            salary_min = base_salary
            salary_max = base_salary + random.randint(20, 40) * 1000
            
            job = models.Job(
                title=title,
                company_id=company.company_id,
                location_id=location.location_id,
                description=f"We are looking for a talented {title} to join our team. "
                           f"You will work on exciting projects using modern technologies.",
                salary_min=salary_min,
                salary_max=salary_max,
                salary_currency="USD",
                salary_period="year",
                job_type="Full-time",
                url=f"https://jobs.example.com/{i}",
                source="sample_data",
                posted_date=posted_date,
                scraped_date=datetime.now()
            )
            db.add(job)
            job_objects.append(job)
            
            # Add random skills to job (3-7 skills per job)
            num_skills = random.randint(3, 7)
            job_skills = random.sample(skill_objects, num_skills)
            job.skills.extend(job_skills)
        
        db.commit()
        print(f"✅ Created {len(job_objects)} jobs with skills")
        
        print("📊 Creating trending insights...")
        # Create trending insights for each skill
        for skill in skill_objects:
            # Count jobs with this skill
            job_count = db.query(models.Job).join(
                models.job_skills,
                models.Job.job_id == models.job_skills.c.job_id
            ).filter(
                models.job_skills.c.skill_id == skill.skill_id
            ).count()
            
            if job_count > 0:
                insight = models.TrendingInsight(
                    skill_id=skill.skill_id,
                    job_count=job_count,
                    growth_rate=random.uniform(-10, 30),  # Random growth rate
                    time_period="30_days",
                    location_id=None
                )
                db.add(insight)
        
        db.commit()
        print("✅ Created trending insights")
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 Data Generation Summary")
        print("=" * 60)
        print(f"Companies: {len(company_objects)}")
        print(f"Locations: {len(location_objects)}")
        print(f"Skills: {len(skill_objects)}")
        print(f"Jobs: {len(job_objects)}")
        print("\n✅ Sample data generation complete!")
        print("\nYou can now:")
        print("1. Start the API: uvicorn api.main:app --reload")
        print("2. Open the website: cd website && python -m http.server 3000")
        print("3. Test the integration: python test_integration.py")
        
    except Exception as e:
        print(f"❌ Error generating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("JobPulse Sample Data Generator")
    print("=" * 60)
    print("\nThis will populate your database with sample data for testing.")
    print("Make sure PostgreSQL is running and configured in .env file.\n")
    
    response = input("Continue? (y/n): ")
    if response.lower() == 'y':
        create_sample_data(num_jobs=100)
    else:
        print("Cancelled.")
