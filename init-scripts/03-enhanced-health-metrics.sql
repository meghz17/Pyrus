-- Enhanced Health Metrics Schema
-- Comprehensive data from Whoop and Oura

-- Whoop Metrics Table
CREATE TABLE IF NOT EXISTS whoop_metrics (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    
    -- Recovery Metrics
    recovery_score INT,
    hrv_rmssd_milli FLOAT,
    resting_heart_rate INT,
    spo2_percentage FLOAT,
    skin_temp_celsius FLOAT,
    
    -- Sleep Metrics
    sleep_performance_percentage INT,
    sleep_consistency_percentage INT,
    sleep_efficiency_percentage FLOAT,
    sleep_duration_minutes INT,
    sleep_needed_minutes INT,
    sleep_debt_minutes INT,
    sleep_disturbances INT,
    rem_sleep_minutes INT,
    deep_sleep_minutes INT,
    light_sleep_minutes INT,
    awake_minutes INT,
    
    -- Strain Metrics
    day_strain FLOAT,
    energy_burned_calories INT,
    avg_heart_rate INT,
    max_heart_rate INT,
    
    -- Cycle Metrics
    cycle_id VARCHAR(100),
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, date)
);

-- Oura Metrics Table
CREATE TABLE IF NOT EXISTS oura_metrics (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    
    -- Readiness Metrics
    readiness_score INT,
    temperature_deviation FLOAT,
    temperature_trend_deviation FLOAT,
    activity_balance INT,
    body_temperature FLOAT,
    hrv_balance INT,
    previous_night_score INT,
    recovery_index INT,
    resting_heart_rate INT,
    sleep_balance INT,
    
    -- Sleep Metrics
    sleep_score INT,
    total_sleep_duration_seconds INT,
    sleep_efficiency INT,
    rem_sleep_duration_seconds INT,
    deep_sleep_duration_seconds INT,
    light_sleep_duration_seconds INT,
    awake_time_seconds INT,
    sleep_latency_seconds INT,
    restlessness FLOAT,
    sleep_timing INT,
    
    -- Activity Metrics
    activity_score INT,
    steps INT,
    active_calories INT,
    total_calories INT,
    target_calories INT,
    met_minutes_high INT,
    met_minutes_medium INT,
    met_minutes_low INT,
    average_met_minutes FLOAT,
    inactivity_alerts INT,
    
    -- Heart Rate Metrics
    avg_hrv FLOAT,
    min_hrv FLOAT,
    max_hrv FLOAT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, date)
);

-- Wellness Scores Table (computed daily)
CREATE TABLE IF NOT EXISTS wellness_scores (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    
    -- Composite Scores
    overall_wellness INT, -- 0-100
    physical_readiness INT, -- 0-100
    energy_level INT, -- 0-100
    mental_clarity INT, -- 0-100
    resilience INT, -- 0-100
    
    -- Trends
    trend_7day VARCHAR(20), -- 'improving', 'stable', 'declining'
    predicted_tomorrow INT, -- 0-100
    
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, date)
);

-- Activity Suggestions Table
CREATE TABLE IF NOT EXISTS activity_suggestions (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    
    -- Joint Scores
    couple_compatibility INT, -- 0-100
    optimal_for_date BOOLEAN,
    optimal_for_workout BOOLEAN,
    
    -- Suggestions
    suggestion_type VARCHAR(50), -- 'date', 'workout', 'rest', 'light_activity'
    suggestion_text TEXT,
    confidence INT, -- 0-100
    
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(date)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_whoop_user_date ON whoop_metrics(user_id, date DESC);
CREATE INDEX IF NOT EXISTS idx_oura_user_date ON oura_metrics(user_id, date DESC);
CREATE INDEX IF NOT EXISTS idx_wellness_user_date ON wellness_scores(user_id, date DESC);
CREATE INDEX IF NOT EXISTS idx_suggestions_date ON activity_suggestions(date DESC);
