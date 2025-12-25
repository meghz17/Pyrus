-- Phase J: Full Metrics Pipeline Redesign
-- Run this SQL in your Supabase SQL Editor

-- 1. Create whoop_metrics table
CREATE TABLE IF NOT EXISTS whoop_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  date DATE NOT NULL UNIQUE,
  fetched_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Recovery
  recovery_score FLOAT,
  resting_hr FLOAT,
  hrv_rmssd FLOAT,
  spo2 FLOAT,
  skin_temp_c FLOAT,
  
  -- Sleep
  sleep_hours FLOAT,
  sleep_performance FLOAT,
  sleep_efficiency FLOAT,
  rem_hours FLOAT,
  deep_hours FLOAT,
  light_hours FLOAT,
  awake_hours FLOAT,
  sleep_cycles INT,
  respiratory_rate FLOAT,
  
  -- Strain
  strain_score FLOAT,
  workout_count INT,
  
  -- Body
  height_m FLOAT,
  weight_kg FLOAT,
  max_hr INT
);

-- 2. Create oura_metrics table
CREATE TABLE IF NOT EXISTS oura_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  date DATE NOT NULL UNIQUE,
  fetched_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Readiness
  readiness_score INT,
  temp_deviation FLOAT,
  hrv_balance INT,
  
  -- Sleep
  sleep_hours FLOAT,
  sleep_efficiency INT,
  rem_hours FLOAT,
  deep_hours FLOAT,
  light_hours FLOAT,
  awake_hours FLOAT,
  latency_minutes FLOAT,
  lowest_hr INT,
  average_hr INT,
  average_hrv INT,
  
  -- Activity
  activity_score INT,
  steps INT,
  active_calories INT,
  high_activity_minutes FLOAT,
  
  -- Stress (Gen3 only)
  stress_high INT,
  recovery_high INT,
  
  -- SpO2
  spo2_avg FLOAT
);

-- 3. Create indexes for date queries
CREATE INDEX IF NOT EXISTS idx_whoop_metrics_date ON whoop_metrics(date DESC);
CREATE INDEX IF NOT EXISTS idx_oura_metrics_date ON oura_metrics(date DESC);

-- 4. Enable RLS but allow authenticated access
ALTER TABLE whoop_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE oura_metrics ENABLE ROW LEVEL SECURITY;

-- Allow all operations for authenticated users (service role bypasses RLS)
CREATE POLICY "Allow service role full access" ON whoop_metrics FOR ALL USING (true);
CREATE POLICY "Allow service role full access" ON oura_metrics FOR ALL USING (true);

COMMENT ON TABLE whoop_metrics IS 'Individual daily metrics from Whoop band';
COMMENT ON TABLE oura_metrics IS 'Individual daily metrics from Oura ring';
