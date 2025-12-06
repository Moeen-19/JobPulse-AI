# api/ml/forecasting.py
import pandas as pd
from sqlalchemy.orm import Session
from datetime import date, timedelta
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)

def run_forecast(db: Session, skill_name: str, region: str = None, days_ahead: int = 30):
    """
    Forecast job growth for a given skill and region using Prophet.
    Note: Prophet import is optional - will use simple trend if not available.
    """
    try:
        from prophet import Prophet
        use_prophet = True
    except ImportError:
        logger.warning("Prophet not available, using simple trend forecasting")
        use_prophet = False
    
    from api import models
    
    # Fetch past data: count of jobs per day for this skill (+ optional region)
    query = (
        db.query(
            func.date(models.Job.posted_date).label('date'),
            func.count(models.Job.job_id).label('job_count')
        )
        .join(models.job_skills, models.Job.job_id == models.job_skills.c.job_id)
        .join(models.Skill, models.job_skills.c.skill_id == models.Skill.skill_id)
        .filter(models.Skill.skill_name.ilike(f"%{skill_name}%"))
        .filter(models.Job.posted_date.isnot(None))
    )

    if region:
        query = query.join(models.Location, models.Job.location_id == models.Location.location_id)
        query = query.filter(models.Location.country.ilike(f"%{region}%"))

    query = query.group_by(func.date(models.Job.posted_date))
    query = query.order_by(func.date(models.Job.posted_date))
    
    data = query.all()

    if not data:
        return {
            "message": f"No data available for skill '{skill_name}' in region '{region or 'global'}'",
            "skill": skill_name,
            "region": region or "global",
            "historical_points": [],
            "forecast_points": []
        }

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["ds", "y"])
    df['ds'] = pd.to_datetime(df['ds'])
    
    historical_data = df.to_dict(orient="records")

    # Forecast using Prophet or simple trend
    if use_prophet and len(df) >= 2:
        try:
            model = Prophet(
                daily_seasonality=False,
                weekly_seasonality=True,
                yearly_seasonality=False
            )
            model.fit(df)

            future = model.make_future_dataframe(periods=days_ahead)
            forecast = model.predict(future)
            
            forecast_data = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(days_ahead)
            forecast_points = forecast_data.to_dict(orient="records")
        except Exception as e:
            logger.error(f"Prophet forecasting failed: {e}")
            forecast_points = simple_trend_forecast(df, days_ahead)
    else:
        forecast_points = simple_trend_forecast(df, days_ahead)

    return {
        "skill": skill_name,
        "region": region or "global",
        "historical_points": historical_data,
        "forecast_points": forecast_points,
        "method": "prophet" if use_prophet else "simple_trend"
    }

def simple_trend_forecast(df: pd.DataFrame, days_ahead: int):
    """Simple linear trend forecasting as fallback"""
    if len(df) < 2:
        return []
    
    # Calculate simple linear trend
    df['days'] = (df['ds'] - df['ds'].min()).dt.days
    slope = (df['y'].iloc[-1] - df['y'].iloc[0]) / (df['days'].iloc[-1] - df['days'].iloc[0]) if df['days'].iloc[-1] > 0 else 0
    intercept = df['y'].iloc[-1] - slope * df['days'].iloc[-1]
    
    # Generate future dates
    last_date = df['ds'].max()
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=days_ahead, freq='D')
    
    forecast_points = []
    for i, future_date in enumerate(future_dates):
        days_from_start = df['days'].iloc[-1] + i + 1
        predicted_value = max(0, slope * days_from_start + intercept)
        
        forecast_points.append({
            "ds": future_date.isoformat(),
            "yhat": predicted_value,
            "yhat_lower": max(0, predicted_value * 0.8),
            "yhat_upper": predicted_value * 1.2
        })
    
    return forecast_points