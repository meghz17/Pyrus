CREATE TABLE IF NOT EXISTS health_metrics (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,          -- 'partner_a' (Whoop) or 'partner_b' (Oura)
    date DATE NOT NULL,
    
    -- Normalized Scores (0-100)
    recovery_score INTEGER,         -- Whoop Recovery / Oura Readiness
    sleep_score INTEGER,
    
    -- Raw Data (for Z-Score Calculation)
    raw_hrv FLOAT,
    raw_rhr FLOAT,
    sleep_hours FLOAT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT unique_daily_metric UNIQUE (user_id, date)
);

CREATE INDEX IF NOT EXISTS idx_health_metrics_date ON health_metrics(date);
