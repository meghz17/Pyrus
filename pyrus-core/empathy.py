import numpy as np
from sqlalchemy.orm import Session
from models import HealthMetricDB
from datetime import date, timedelta

def calculate_z_score(value, history):
    if not history or len(history) < 5:
        return 0.0 # Not enough data
    
    mean = np.mean(history)
    std = np.std(history)
    
    if std == 0:
        return 0.0
        
    return (value - mean) / std

def get_couple_battery_status(db: Session, today: date):
    # Get last 30 days for both partners
    start_date = today - timedelta(days=30)
    
    metrics = db.query(HealthMetricDB).filter(
        HealthMetricDB.date >= start_date
    ).all()
    
    partner_a_data = [m for m in metrics if m.user_id == 'partner_a']
    partner_b_data = [m for m in metrics if m.user_id == 'partner_b']
    
    # Get today's values
    today_a = next((m for m in partner_a_data if m.date == today), None)
    today_b = next((m for m in partner_b_data if m.date == today), None)
    
    if not today_a or not today_b:
        return {"status": "insufficient_data", "message": "Missing data for today"}

    # Extract histories
    history_a = [m.recovery_score for m in partner_a_data if m.date != today and m.recovery_score is not None]
    history_b = [m.recovery_score for m in partner_b_data if m.date != today and m.recovery_score is not None]
    
    # Calculate Z-Scores
    z_a = calculate_z_score(today_a.recovery_score, history_a)
    z_b = calculate_z_score(today_b.recovery_score, history_b)
    
    # Normalize to 0-100 scale (Z=-2 -> 10, Z=0 -> 50, Z=+2 -> 90)
    norm_a = max(0, min(100, 50 + (z_a * 20)))
    norm_b = max(0, min(100, 50 + (z_b * 20)))
    
    # Empathy Checks
    gap = abs(norm_a - norm_b)
    avg_energy = (norm_a + norm_b) / 2
    
    status = "Normal"
    action = "None"
    
    if avg_energy < 40:
        status = "Survival Mode"
        action = "Reschedule Chores"
    elif gap > 30:
        status = "Energy Imbalance"
        action = "Nudge High Energy Partner"
        
    return {
        "date": today.isoformat(),
        "partner_a": {"raw": today_a.recovery_score, "z_score": round(z_a, 2), "normalized": round(norm_a)},
        "partner_b": {"raw": today_b.recovery_score, "z_score": round(z_b, 2), "normalized": round(norm_b)},
        "joint_status": status,
        "recommended_action": action
    }
