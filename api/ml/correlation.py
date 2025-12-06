# api/ml/correlation.py
import pandas as pd
from sqlalchemy.orm import Session
from itertools import combinations
from collections import Counter
import logging

logger = logging.getLogger(__name__)

def run_correlation(db: Session, region: str = None, top_n: int = 20):
    """
    Find skill-to-skill correlations based on co-occurrence in job postings.
    """
    from api import models
    
    # Query to get job_id and skill names
    query = (
        db.query(
            models.Job.job_id,
            models.Skill.skill_name
        )
        .join(models.job_skills, models.Job.job_id == models.job_skills.c.job_id)
        .join(models.Skill, models.job_skills.c.skill_id == models.Skill.skill_id)
    )

    if region:
        query = query.join(models.Location, models.Job.location_id == models.Location.location_id)
        query = query.filter(models.Location.country.ilike(f"%{region}%"))

    data = query.all()
    
    if not data:
        return {
            "message": f"No data for region '{region or 'global'}'",
            "correlations": []
        }

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["job_id", "skill"])

    # Group by job, collect all skills for each job
    grouped = df.groupby("job_id")["skill"].apply(list)

    # Count co-occurrences
    pair_counts = Counter()
    for skill_list in grouped:
        unique_skills = set(skill_list)
        if len(unique_skills) >= 2:
            for pair in combinations(sorted(unique_skills), 2):
                pair_counts[pair] += 1

    if not pair_counts:
        return {
            "message": "No skill correlations found",
            "correlations": []
        }

    # Get top N correlations
    top_correlations = [
        {"skill_1": a, "skill_2": b, "count": c}
        for (a, b), c in pair_counts.most_common(top_n)
    ]

    return {
        "region": region or "global",
        "total_jobs": len(grouped),
        "total_correlations": len(pair_counts),
        "correlations": top_correlations
    }