import os
from whoop_client import WhoopClient
from datetime import datetime

client = WhoopClient(
    client_id=os.getenv("WHOOP_CLIENT_ID"),
    client_secret=os.getenv("WHOOP_CLIENT_SECRET")
)

print("\n" + "="*60)
print("🏃 YOUR WHOOP DATA SUMMARY")
print("="*60)

# Body Measurements
print("\n📊 BODY MEASUREMENTS")
print("-"*60)
body = client.get_body_measurements()
height_m = body.get('height_meter', 0)
height_ft = int(height_m * 3.28084 // 1)
height_in = int((height_m * 3.28084 % 1) * 12)
weight_kg = body.get('weight_kilogram', 0)
weight_lbs = int(weight_kg * 2.20462)
print(f"Height: {height_m}m ({height_ft}'{height_in}\")")
print(f"Weight: {weight_kg}kg ({weight_lbs} lbs)")
print(f"Max HR: {body.get('max_heart_rate')} bpm")

# Latest Recovery
print("\n💚 LATEST RECOVERY")
print("-"*60)
recovery = client.get_recovery(limit=1)
if recovery.get('records'):
    r = recovery['records'][0]
    score_data = r.get('score', {})
    print(f"Recovery Score: {score_data.get('recovery_score')}%")
    print(f"Resting HR: {score_data.get('resting_heart_rate')} bpm")
    print(f"HRV (RMSSD): {score_data.get('hrv_rmssd_milli'):.1f} ms")
    print(f"SpO2: {score_data.get('spo2_percentage')}%")
    print(f"Skin Temp: {score_data.get('skin_temp_celsius'):.1f}°C")

# Latest Sleep
print("\n😴 LATEST SLEEP")
print("-"*60)
sleep = client.get_sleep(limit=1)
if sleep.get('records'):
    s = sleep['records'][0]
    score_data = s.get('score', {})
    stages = score_data.get('stage_summary', {})
    
    total_sleep = stages.get('total_in_bed_time_milli', 0) / 1000 / 60 / 60
    rem = stages.get('total_rem_sleep_time_milli', 0) / 1000 / 60 / 60
    deep = stages.get('total_slow_wave_sleep_time_milli', 0) / 1000 / 60 / 60
    light = stages.get('total_light_sleep_time_milli', 0) / 1000 / 60 / 60
    
    print(f"Total Time in Bed: {total_sleep:.1f} hours")
    print(f"Sleep Performance: {score_data.get('sleep_performance_percentage')}%")
    print(f"Sleep Efficiency: {score_data.get('sleep_efficiency_percentage'):.1f}%")
    print(f"  • REM: {rem:.1f}h | Deep: {deep:.1f}h | Light: {light:.1f}h")
    print(f"Sleep Cycles: {stages.get('sleep_cycle_count')}")
    print(f"Respiratory Rate: {score_data.get('respiratory_rate'):.1f} breaths/min")

# Latest Workout
print("\n🏋️ LATEST WORKOUT")
print("-"*60)
workouts = client.get_workouts(limit=1)
if workouts.get('records'):
    w = workouts['records'][0]
    score_data = w.get('score', {})
    duration_hours = (
        datetime.fromisoformat(w['end'].replace('Z', '+00:00')) - 
        datetime.fromisoformat(w['start'].replace('Z', '+00:00'))
    ).total_seconds() / 3600
    
    print(f"Activity: {w.get('sport_name', 'N/A')}")
    print(f"Duration: {duration_hours:.1f} hours")
    print(f"Strain: {score_data.get('strain'):.1f}")
    print(f"Avg HR: {score_data.get('average_heart_rate')} bpm")
    print(f"Max HR: {score_data.get('max_heart_rate')} bpm")
    print(f"Calories: {score_data.get('kilojoule', 0) / 4.184:.0f} kcal")

print("\n" + "="*60)
print("✓ Data retrieved successfully!")
print("="*60 + "\n")
