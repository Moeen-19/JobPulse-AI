# api/ml/correlation.py
import pandas as pd
from sqlalchemy.orm import Session
from itertools import combinations
from collections import Counter
from api import models

def run_correlation(db: Session, region: str = None, top_n: int = 20):
    """
    Find skill-to-skill correlations based on co-occurrence in job postings.
    """
    query = (
        db.query(models.Job.id, models.Location.country, models.Skill.name)
        .join(models.Job.skills)
        .join(models.Job.location)
    )

    if region:
        query = query.filter(models.Location.country.ilike(f"%{region}%"))

    data = query.all()
    if not data:
        return {"message": f"No data for region '{region}'"}

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["job_id", "country", "skill"])

    # Group by job, collect all skills for each job
    grouped = df.groupby("job_id")["skill"].apply(list)

    # Count co-occurrences
    pair_counts = Counter()
    for skill_list in grouped:
        for pair in combinations(sorted(set(skill_list)), 2):
            pair_counts[pair] += 1

    # Convert to sorted DataFrame
    corr_df = pd.DataFrame(pair_counts.items(), columns=["pair", "count"])
    corr_df = corr_df.sort_values("count", ascending=False).head(top_n)

    return [
        {"skill_1": a, "skill_2": b, "count": c}
        for (a, b), c in pair_counts.most_common(top_n)
    ]