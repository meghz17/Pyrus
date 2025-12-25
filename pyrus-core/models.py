from sqlalchemy import Column, Integer, String, Float, Date, Boolean, Text, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from database import Base

# Legacy model for backward compatibility
class HealthMetricDB(Base):
    __tablename__ = "health_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    recovery_score = Column(Integer)
    sleep_score = Column(Integer)
    raw_hrv = Column(Float)
    raw_rhr = Column(Float)
    sleep_hours = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    
    __table_args__ = (UniqueConstraint('user_id', 'date', name='_health_user_date_uc'),)

class WhoopMetrics(Base):

    __tablename__ = "whoop_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    
    # Recovery
    recovery_score = Column(Integer)
    hrv_rmssd_milli = Column(Float)
    resting_heart_rate = Column(Integer)
    spo2_percentage = Column(Float)
    skin_temp_celsius = Column(Float)
    
    # Sleep
    sleep_performance_percentage = Column(Integer)
    sleep_consistency_percentage = Column(Integer)
    sleep_efficiency_percentage = Column(Float)
    sleep_duration_minutes = Column(Integer)
    sleep_needed_minutes = Column(Integer)
    sleep_debt_minutes = Column(Integer)
    sleep_disturbances = Column(Integer)
    rem_sleep_minutes = Column(Integer)
    deep_sleep_minutes = Column(Integer)
    light_sleep_minutes = Column(Integer)
    awake_minutes = Column(Integer)
    
    # Strain
    day_strain = Column(Float)
    energy_burned_calories = Column(Integer)
    avg_heart_rate = Column(Integer)
    max_heart_rate = Column(Integer)
    
    # Cycle
    cycle_id = Column(String(100))
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (UniqueConstraint('user_id', 'date', name='_whoop_user_date_uc'),)


class OuraMetrics(Base):
    __tablename__ = "oura_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    
    # Readiness
    readiness_score = Column(Integer)
    temperature_deviation = Column(Float)
    temperature_trend_deviation = Column(Float)
    activity_balance = Column(Integer)
    body_temperature = Column(Float)
    hrv_balance = Column(Integer)
    previous_night_score = Column(Integer)
    recovery_index = Column(Integer)
    resting_heart_rate = Column(Integer)
    sleep_balance = Column(Integer)
    
    # Sleep
    sleep_score = Column(Integer)
    total_sleep_duration_seconds = Column(Integer)
    sleep_efficiency = Column(Integer)
    rem_sleep_duration_seconds = Column(Integer)
    deep_sleep_duration_seconds = Column(Integer)
    light_sleep_duration_seconds = Column(Integer)
    awake_time_seconds = Column(Integer)
    sleep_latency_seconds = Column(Integer)
    restlessness = Column(Float)
    sleep_timing = Column(Integer)
    
    # Activity
    activity_score = Column(Integer)
    steps = Column(Integer)
    active_calories = Column(Integer)
    total_calories = Column(Integer)
    target_calories = Column(Integer)
    met_minutes_high = Column(Integer)
    met_minutes_medium = Column(Integer)
    met_minutes_low = Column(Integer)
    average_met_minutes = Column(Float)
    inactivity_alerts = Column(Integer)
    
    # Heart Rate
    avg_hrv = Column(Float)
    min_hrv = Column(Float)
    max_hrv = Column(Float)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (UniqueConstraint('user_id', 'date', name='_oura_user_date_uc'),)


class WellnessScore(Base):
    __tablename__ = "wellness_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    
    # Composite Scores
    overall_wellness = Column(Integer)  # 0-100
    physical_readiness = Column(Integer)  # 0-100
    energy_level = Column(Integer)  # 0-100
    mental_clarity = Column(Integer)  # 0-100
    resilience = Column(Integer)  # 0-100
    
    # Trends
    trend_7day = Column(String(20))  # 'improving', 'stable', 'declining'
    predicted_tomorrow = Column(Integer)  # 0-100
    
    created_at = Column(DateTime, server_default=func.now())
    
    __table_args__ = (UniqueConstraint('user_id', 'date', name='_wellness_user_date_uc'),)


class ActivitySuggestion(Base):
    __tablename__ = "activity_suggestions"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True)
    
    # Joint Scores
    couple_compatibility = Column(Integer)  # 0-100
    optimal_for_date = Column(Boolean)
    optimal_for_workout = Column(Boolean)
    
    # Suggestions
    suggestion_type = Column(String(50))  # 'date', 'workout', 'rest', 'light_activity'
    suggestion_text = Column(Text)
    confidence = Column(Integer)  # 0-100
    
    created_at = Column(DateTime, server_default=func.now())
