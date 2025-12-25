from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

# Local Imports
from database import get_db, engine, Base
from models import HealthMetricDB, WhoopMetrics, OuraMetrics, WellnessScore
import empathy
import wellness
import suggestions

# Initialize DB Tables
Base.metadata.create_all(bind=engine)

# --- Pydantic Schemas ---
class IngestPayload(BaseModel):
    user_id: str = Field(..., pattern="^(partner_a|partner_b)$")
    date: date
    recovery_score: int
    sleep_score: int
    raw_hrv: float
    raw_rhr: float
    sleep_hours: float

class WhoopPayload(BaseModel):
    user_id: str
    date: date
    # Recovery
    recovery_score: Optional[int] = None
    hrv_rmssd_milli: Optional[float] = None
    resting_heart_rate: Optional[int] = None
    spo2_percentage: Optional[float] = None
    skin_temp_celsius: Optional[float] = None
    # Sleep
    sleep_performance_percentage: Optional[int] = None
    sleep_consistency_percentage: Optional[int] = None
    sleep_efficiency_percentage: Optional[float] = None
    sleep_duration_minutes: Optional[int] = None
    sleep_needed_minutes: Optional[int] = None
    sleep_debt_minutes: Optional[int] = None
    sleep_disturbances: Optional[int] = None
    rem_sleep_minutes: Optional[int] = None
    deep_sleep_minutes: Optional[int] = None
    light_sleep_minutes: Optional[int] = None
    awake_minutes: Optional[int] = None
    # Strain
    day_strain: Optional[float] = None
    energy_burned_calories: Optional[int] = None
    avg_heart_rate: Optional[int] = None
    max_heart_rate: Optional[int] = None
    cycle_id: Optional[str] = None

class OuraPayload(BaseModel):
    user_id: str
    date: date
    # Readiness
    readiness_score: Optional[int] = None
    temperature_deviation: Optional[float] = None
    temperature_trend_deviation: Optional[float] = None
    activity_balance: Optional[int] = None
    body_temperature: Optional[float] = None
    hrv_balance: Optional[int] = None
    previous_night_score: Optional[int] = None
    recovery_index: Optional[int] = None
    resting_heart_rate: Optional[int] = None
    sleep_balance: Optional[int] = None
    # Sleep
    sleep_score: Optional[int] = None
    total_sleep_duration_seconds: Optional[int] = None
    sleep_efficiency: Optional[int] = None
    rem_sleep_duration_seconds: Optional[int] = None
    deep_sleep_duration_seconds: Optional[int] = None
    light_sleep_duration_seconds: Optional[int] = None
    awake_time_seconds: Optional[int] = None
    sleep_latency_seconds: Optional[int] = None
    restlessness: Optional[float] = None
    sleep_timing: Optional[int] = None
    # Activity
    activity_score: Optional[int] = None
    steps: Optional[int] = None
    active_calories: Optional[int] = None
    total_calories: Optional[int] = None
    target_calories: Optional[int] = None
    met_minutes_high: Optional[int] = None
    met_minutes_medium: Optional[int] = None
    met_minutes_low: Optional[int] = None
    average_met_minutes: Optional[float] = None
    inactivity_alerts: Optional[int] = None
    # Heart Rate
    avg_hrv: Optional[float] = None
    min_hrv: Optional[float] = None
    max_hrv: Optional[float] = None

# --- FastAPI App ---
app = FastAPI(
    title="Pyrus V2 Cortex API",
    description="The intelligence layer for the Pyrus Agentic System",
    version="2.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "system": "Pyrus V2 Cortex", "version": "2.2.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# --- Legacy Endpoint (for backward compatibility) ---
@app.post("/api/ingest/health")
def ingest_health_metric(payload: IngestPayload, db: Session = Depends(get_db)):
    """Legacy endpoint - still supported"""
    try:
        existing = db.query(HealthMetricDB).filter(
            HealthMetricDB.user_id == payload.user_id,
            HealthMetricDB.date == payload.date
        ).first()

        if existing:
            existing.recovery_score = payload.recovery_score
            existing.sleep_score = payload.sleep_score
            existing.raw_hrv = payload.raw_hrv
            existing.raw_rhr = payload.raw_rhr
            existing.sleep_hours = payload.sleep_hours
        else:
            new_record = HealthMetricDB(**payload.dict())
            db.add(new_record)
        
        db.commit()
        return {"status": "success", "message": f"Data saved for {payload.user_id}"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# --- New Enhanced Endpoints ---
@app.post("/api/ingest/whoop")
def ingest_whoop_metrics(payload: WhoopPayload, db: Session = Depends(get_db)):
    """Ingest comprehensive Whoop metrics"""
    try:
        existing = db.query(WhoopMetrics).filter(
            WhoopMetrics.user_id == payload.user_id,
            WhoopMetrics.date == payload.date
        ).first()

        if existing:
            for key, value in payload.dict(exclude_unset=True).items():
                setattr(existing, key, value)
        else:
            new_record = WhoopMetrics(**payload.dict(exclude_unset=True))
            db.add(new_record)
        
        db.commit()
        return {"status": "success", "message": f"Whoop data saved for {payload.user_id}"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ingest/oura")
def ingest_oura_metrics(payload: OuraPayload, db: Session = Depends(get_db)):
    """Ingest comprehensive Oura metrics"""
    try:
        existing = db.query(OuraMetrics).filter(
            OuraMetrics.user_id == payload.user_id,
            OuraMetrics.date == payload.date
        ).first()

        if existing:
            for key, value in payload.dict(exclude_unset=True).items():
                setattr(existing, key, value)
        else:
            new_record = OuraMetrics(**payload.dict(exclude_unset=True))
            db.add(new_record)
        
        db.commit()
        return {"status": "success", "message": f"Oura data saved for {payload.user_id}"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/wellness/daily")
def get_daily_wellness(target_date: date = date.today(), db: Session = Depends(get_db)):
    """Calculate and return daily wellness scores for both partners"""
    try:
        # Calculate for both partners
        partner_a_wellness = wellness.calculate_wellness_score("partner_a", target_date, db)
        partner_b_wellness = wellness.calculate_wellness_score("partner_b", target_date, db)
        
        if partner_a_wellness.get("status") == "insufficient_data" or \
           partner_b_wellness.get("status") == "insufficient_data":
            return {
                "status": "insufficient_data",
                "message": "Missing data for one or both partners"
            }
        
        # Save to database (UPSERT logic)
        for user_id, wellness_data in [("partner_a", partner_a_wellness), ("partner_b", partner_b_wellness)]:
            existing = db.query(WellnessScore).filter(
                WellnessScore.user_id == user_id,
                WellnessScore.date == target_date
            ).first()
            
            if existing:
                # Update existing record
                for key, value in wellness_data.items():
                    setattr(existing, key, value)
            else:
                # Insert new record
                score = WellnessScore(
                    user_id=user_id,
                    date=target_date,
                    **wellness_data
                )
                db.add(score)
        
        db.commit()
        
        return {
            "date": target_date.isoformat(),
            "partner_a": partner_a_wellness,
            "partner_b": partner_b_wellness
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/suggestions")
def get_activity_suggestions(target_date: date = date.today(), db: Session = Depends(get_db)):
    """Generate activity suggestions based on wellness scores"""
    try:
        result = suggestions.generate_suggestions(target_date, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Legacy Empathy Endpoint ---
@app.get("/api/calc/empathy")
def get_daily_empathy_score(target_date: date = date.today(), db: Session = Depends(get_db)):
    """Legacy empathy calculation - still supported"""
    try:
        result = empathy.get_couple_battery_status(db, target_date)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
