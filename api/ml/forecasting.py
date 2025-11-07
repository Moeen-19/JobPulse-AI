# api/ml/forecasting.py
import pandas as pd
from prophet import Prophet
from sqlalchemy.orm import Session
from datetime import date, timedelta
from api import models

def run_forecast(db: Session, skill_name: str, region: str = None, days_ahead: int = 30):
    """
    Forecast job growth for a given skill and region using Prophet.
    """
    # Fetch past data: count of jobs per day for this skill (+ optional region)
    query = (
        db.query(models.Job.posted_date, models.Location.country, models.Skill.name)
        .join(models.Job.skills)
        .join(models.Job.location)
        .filter(models.Skill.name.ilike(f"%{skill_name}%"))
    )

    if region:
        query = query.filter(models.Location.country.ilike(f"%{region}%"))

    data = query.all()

    if not data:
        return {"message": f"No data available for skill '{skill_name}' in region '{region}'"}

    # Aggregate job counts per day
    df = pd.DataFrame(data, columns=["date", "country", "skill"])
    df = df.groupby("date").size().reset_index(name="job_count")
    df.rename(columns={"date": "ds", "job_count": "y"}, inplace=True)

    # Forecast
    model = Prophet(daily_seasonality=True)
    model.fit(df)

    future = model.make_future_dataframe(periods=days_ahead)
    forecast = model.predict(future)

    return {
        "skill": skill_name,
        "region": region or "global",
        "historical_points": df.to_dict(orient="records"),
        "forecast_points": forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(days_ahead).to_dict(orient="records")
    }