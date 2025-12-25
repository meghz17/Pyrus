"""
Holistic Wellness Scoring Algorithm
Multi-dimensional health assessment based on comprehensive metrics
"""
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import WhoopMetrics, OuraMetrics, WellnessScore
import statistics


def calculate_wellness_score(
    user_id: str,
    date: datetime.date,
    db: Session
) -> Dict:
    """
    Calculate holistic wellness score from all available metrics
    
    Returns:
        {
            "overall_wellness": 0-100,
            "physical_readiness": 0-100,
            "energy_level": 0-100,
            "mental_clarity": 0-100,
            "resilience": 0-100,
            "trend_7day": "improving|stable|declining",
            "predicted_tomorrow": 0-100
        }
    """
    
    # Fetch metrics
    whoop = db.query(WhoopMetrics).filter(
        WhoopMetrics.user_id == user_id,
        WhoopMetrics.date == date
    ).first()
    
    oura = db.query(OuraMetrics).filter(
        OuraMetrics.user_id == user_id,
        OuraMetrics.date == date
    ).first()
    
    if not whoop and not oura:
        return {
            "status": "insufficient_data",
            "message": f"No data for {user_id} on {date}"
        }
    
    # Calculate dimension scores
    physical = _calculate_physical_readiness(whoop, oura)
    energy = _calculate_energy_level(whoop, oura)
    mental = _calculate_mental_clarity(whoop, oura)
    resilience = _calculate_resilience(whoop, oura)
    
    # Weighted composite score
    overall = int(
        physical * 0.40 +
        energy * 0.30 +
        mental * 0.20 +
        resilience * 0.10
    )
    
    # Calculate trend
    trend = _calculate_trend(user_id, date, db)
    predicted = _predict_tomorrow(user_id, date, db)
    
    return {
        "overall_wellness": overall,
        "physical_readiness": physical,
        "energy_level": energy,
        "mental_clarity": mental,
        "resilience": resilience,
        "trend_7day": trend,
        "predicted_tomorrow": predicted
    }


def _calculate_physical_readiness(whoop: Optional[WhoopMetrics], oura: Optional[OuraMetrics]) -> int:
    """Physical Readiness (40% weight)"""
    scores = []
    
    if whoop:
        if whoop.recovery_score:
            scores.append(whoop.recovery_score)
        if whoop.hrv_rmssd_milli:
            # Normalize HRV (typical range 20-100ms)
            scores.append(min(100, (whoop.hrv_rmssd_milli / 100) * 100))
        if whoop.resting_heart_rate:
            # Lower RHR is better (typical range 40-80 bpm)
            scores.append(max(0, 100 - ((whoop.resting_heart_rate - 40) * 2.5)))
    
    if oura:
        if oura.readiness_score:
            scores.append(oura.readiness_score)
        if oura.hrv_balance:
            scores.append(oura.hrv_balance)
    
    return int(statistics.mean(scores)) if scores else 50


def _calculate_energy_level(whoop: Optional[WhoopMetrics], oura: Optional[OuraMetrics]) -> int:
    """Energy Level (30% weight)"""
    scores = []
    
    if whoop:
        if whoop.day_strain:
            # Lower strain = more energy available (typical range 0-21)
            scores.append(max(0, 100 - (whoop.day_strain * 5)))
        if whoop.sleep_performance_percentage:
            scores.append(whoop.sleep_performance_percentage)
    
    if oura:
        if oura.activity_score:
            scores.append(oura.activity_score)
        if oura.sleep_balance:
            scores.append(oura.sleep_balance)
    
    return int(statistics.mean(scores)) if scores else 50


def _calculate_mental_clarity(whoop: Optional[WhoopMetrics], oura: Optional[OuraMetrics]) -> int:
    """Mental Clarity (20% weight)"""
    scores = []
    
    if whoop:
        if whoop.sleep_efficiency_percentage:
            scores.append(whoop.sleep_efficiency_percentage)
        if whoop.rem_sleep_minutes and whoop.sleep_duration_minutes:
            # REM should be 20-25% of total sleep
            rem_percentage = (whoop.rem_sleep_minutes / whoop.sleep_duration_minutes) * 100
            scores.append(min(100, rem_percentage * 4.5))  # Normalize to 100
        if whoop.sleep_disturbances:
            # Fewer disturbances = better (typical range 0-20)
            scores.append(max(0, 100 - (whoop.sleep_disturbances * 5)))
    
    if oura:
        if oura.sleep_score:
            scores.append(oura.sleep_score)
        if oura.sleep_efficiency:
            scores.append(oura.sleep_efficiency)
    
    return int(statistics.mean(scores)) if scores else 50


def _calculate_resilience(whoop: Optional[WhoopMetrics], oura: Optional[OuraMetrics]) -> int:
    """Resilience (10% weight)"""
    scores = []
    
    if whoop:
        if whoop.spo2_percentage:
            # SpO2 should be 95-100%
            scores.append(min(100, (whoop.spo2_percentage - 90) * 10))
        if whoop.skin_temp_celsius:
            # Stable temp is good (deviation from baseline)
            # Assuming baseline ~36.5°C, deviation < 0.5°C is good
            deviation = abs(whoop.skin_temp_celsius - 36.5)
            scores.append(max(0, 100 - (deviation * 100)))
    
    if oura:
        if oura.temperature_deviation:
            # Lower deviation is better
            scores.append(max(0, 100 - (abs(oura.temperature_deviation) * 50)))
        if oura.recovery_index:
            scores.append(oura.recovery_index)
    
    return int(statistics.mean(scores)) if scores else 50


def _calculate_trend(user_id: str, date: datetime.date, db: Session) -> str:
    """Calculate 7-day trend"""
    start_date = date - timedelta(days=7)
    
    scores = db.query(WellnessScore.overall_wellness).filter(
        WellnessScore.user_id == user_id,
        WellnessScore.date >= start_date,
        WellnessScore.date < date
    ).order_by(WellnessScore.date).all()
    
    if len(scores) < 3:
        return "stable"
    
    values = [s[0] for s in scores]
    first_half = statistics.mean(values[:len(values)//2])
    second_half = statistics.mean(values[len(values)//2:])
    
    diff = second_half - first_half
    
    if diff > 5:
        return "improving"
    elif diff < -5:
        return "declining"
    else:
        return "stable"


def _predict_tomorrow(user_id: str, date: datetime.date, db: Session) -> int:
    """Simple linear prediction based on 7-day trend"""
    start_date = date - timedelta(days=7)
    
    scores = db.query(WellnessScore.overall_wellness).filter(
        WellnessScore.user_id == user_id,
        WellnessScore.date >= start_date,
        WellnessScore.date <= date
    ).order_by(WellnessScore.date).all()
    
    if len(scores) < 2:
        return 50  # Default
    
    values = [s[0] for s in scores]
    
    # Simple moving average
    return int(statistics.mean(values[-3:]))  # Average of last 3 days
