#!/usr/bin/env python3
"""
Daily Oura Data Fetcher for MagicMirror Integration

This script fetches the latest Oura Ring health metrics (readiness, sleep, and activity)
and saves them to a JSON file suitable for use with MagicMirror modules.

USAGE:
    python fetch_daily_oura.py
    ./fetch_daily_oura.py  (if made executable with chmod +x)

CRON SCHEDULING:
    # Fetch Oura data every morning at 8:00 AM
    0 8 * * * /usr/bin/python3 /path/to/fetch_daily_oura.py

    # Fetch multiple times per day
    0 8,14,20 * * * /usr/bin/python3 /path/to/fetch_daily_oura.py

REQUIREMENTS:
    - OURA_ACCESS_TOKEN environment variable
    - Active Oura Ring account with authorized API access
    - Get your Personal Access Token from: https://cloud.ouraring.com/personal-access-tokens
"""

import os
import json
import sys
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from oura_client import OuraClient


def safe_get(data: Dict, *keys, default=None) -> Any:
    """Safely navigate nested dictionary keys."""
    result = data
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
        else:
            return default
        if result is None:
            return default
    return result


def fetch_readiness_data(client: OuraClient) -> Optional[Dict[str, Any]]:
    """Fetch the latest readiness data."""
    try:
        readiness = client.get_daily_readiness()
        if not readiness.get('data'):
            print("⚠ No readiness data available")
            return None
        
        r = readiness['data'][0]
        contributors = r.get('contributors', {})
        
        # Get actual resting HR from sleep data (lowest_heart_rate is the true resting HR)
        resting_hr_value = None
        try:
            sleep = client.get_sleep(limit=1)
            if sleep.get('data'):
                resting_hr_value = safe_get(sleep['data'][0], 'lowest_heart_rate')
        except Exception:
            pass
        
        # Get SpO2 data
        spo2_value = None
        try:
            spo2_data = client.get_daily_spo2()
            if spo2_data.get('data'):
                spo2_value = safe_get(spo2_data['data'][0], 'spo2_percentage', 'average')
        except Exception:
            pass
        
        return {
            "score": safe_get(r, 'score'),
            "temperature_deviation": safe_get(r, 'temperature_deviation'),
            "resting_hr": resting_hr_value,  # Actual BPM from sleep data
            "hrv_balance": safe_get(contributors, 'hrv_balance'),  # This is a score 0-100
            "spo2": spo2_value
        }
    except Exception as e:
        print(f"✗ Error fetching readiness data: {e}")
        return None


def fetch_sleep_data(client: OuraClient) -> Optional[Dict[str, Any]]:
    """Fetch the latest sleep data."""
    try:
        sleep = client.get_sleep(limit=1)
        if not sleep.get('data'):
            print("⚠ No sleep data available")
            return None
        
        s = sleep['data'][0]
        
        total_sleep_duration = safe_get(s, 'total_sleep_duration')
        rem_sleep_duration = safe_get(s, 'rem_sleep_duration')
        deep_sleep_duration = safe_get(s, 'deep_sleep_duration')
        light_sleep_duration = safe_get(s, 'light_sleep_duration')
        awake_time = safe_get(s, 'awake_time')
        latency = safe_get(s, 'latency')
        
        return {
            "total_hours": round(total_sleep_duration / 3600, 2) if total_sleep_duration else None,
            "efficiency": safe_get(s, 'efficiency'),
            "rem_hours": round(rem_sleep_duration / 3600, 2) if rem_sleep_duration else None,
            "deep_hours": round(deep_sleep_duration / 3600, 2) if deep_sleep_duration else None,
            "light_hours": round(light_sleep_duration / 3600, 2) if light_sleep_duration else None,
            "awake_time": round(awake_time / 3600, 2) if awake_time else None,
            "latency_minutes": round(latency / 60, 2) if latency else None
        }
    except Exception as e:
        print(f"✗ Error fetching sleep data: {e}")
        return None


def fetch_activity_data(client: OuraClient) -> Optional[Dict[str, Any]]:
    """Fetch the latest activity data."""
    try:
        activity = client.get_daily_activity()
        if not activity.get('data'):
            print("⚠ No activity data available")
            return None
        
        a = activity['data'][0]
        contributors = a.get('contributors', {})
        
        high_activity_time = safe_get(a, 'high_activity_time', default=0)
        active_minutes = round(high_activity_time / 60, 2) if high_activity_time else None
        
        move_every_hour = safe_get(contributors, 'move_every_hour')
        inactivity_alerts = None
        if move_every_hour is not None:
            inactivity_alerts = max(0, round((100 - move_every_hour) / 100 * 24))
        
        return {
            "score": safe_get(a, 'score'),
            "steps": safe_get(a, 'steps'),
            "calories_burned": safe_get(a, 'active_calories'),
            "active_minutes": active_minutes,
            "inactivity_alerts": inactivity_alerts
        }
    except Exception as e:
        print(f"✗ Error fetching activity data: {e}")
        return None


def fetch_stress_data(client: OuraClient) -> Optional[Dict[str, Any]]:
    """Fetch daily stress data (Gen3 ring only)."""
    try:
        stress = client.get_daily_stress()
        if not stress.get('data'):
            return None  # No stress data (likely Gen2 ring)
        s = stress['data'][0]
        return {
            "stress_high": s.get("stress_high"),
            "recovery_high": s.get("recovery_high"),
            "day_summary": s.get("day_summary")
        }
    except Exception:
        return None  # Silently fail for Gen2 rings


def fetch_workout_data(client: OuraClient) -> Optional[Dict[str, Any]]:
    """Fetch detected workouts."""
    try:
        workouts = client.get_workouts()
        if not workouts.get('data'):
            return None
        return {
            "count": len(workouts['data']),
            "workouts": [
                {
                    "activity": w.get("activity"),
                    "calories": w.get("calories"),
                    "duration_minutes": round(w.get("duration", 0) / 60, 1) if w.get("duration") else None
                } for w in workouts['data'][:5]  # Limit to 5 recent
            ]
        }
    except Exception:
        return None


def fetch_hrv_data(client: OuraClient) -> Optional[Dict[str, Any]]:
    """Fetch heart rate variability and HR details from sleep data."""
    try:
        sleep = client.get_sleep(limit=1)
        if not sleep.get('data'):
            return None
        s = sleep['data'][0]
        return {
            "average_hrv": s.get("average_hrv"),
            "lowest_hr": s.get("lowest_heart_rate"),
            "average_hr": s.get("average_heart_rate")
        }
    except Exception:
        return None


def print_summary(data: Dict[str, Any]) -> None:
    """Print a human-readable summary of the fetched data."""
    print("\n" + "="*60)
    print("📊 OURA DATA FETCH SUMMARY")
    print("="*60)
    
    oura = data.get('oura', {})
    
    readiness = oura.get('readiness', {})
    if readiness:
        print("\n💚 READINESS")
        print(f"  Score: {readiness.get('score', 'N/A')}%")
        print(f"  Temperature Deviation: {readiness.get('temperature_deviation', 'N/A')}°C")
        print(f"  Resting HR Score: {readiness.get('resting_hr', 'N/A')}")
        print(f"  HRV Balance: {readiness.get('hrv_balance', 'N/A')}")
        print(f"  SpO2: {readiness.get('spo2', 'N/A')}%")
    
    sleep = oura.get('sleep', {})
    if sleep:
        print("\n😴 SLEEP")
        print(f"  Total Sleep: {sleep.get('total_hours', 'N/A')}h")
        print(f"  Efficiency: {sleep.get('efficiency', 'N/A')}%")
        print(f"  REM: {sleep.get('rem_hours', 'N/A')}h | Deep: {sleep.get('deep_hours', 'N/A')}h | Light: {sleep.get('light_hours', 'N/A')}h")
        print(f"  Awake Time: {sleep.get('awake_time', 'N/A')}h")
        print(f"  Latency: {sleep.get('latency_minutes', 'N/A')} min")
    
    activity = oura.get('activity', {})
    if activity:
        print("\n🏃 ACTIVITY")
        print(f"  Score: {activity.get('score', 'N/A')}%")
        print(f"  Steps: {activity.get('steps', 'N/A')}")
        print(f"  Calories Burned: {activity.get('calories_burned', 'N/A')} kcal")
        print(f"  Active Minutes: {activity.get('active_minutes', 'N/A')}")
        print(f"  Inactivity Alerts: {activity.get('inactivity_alerts', 'N/A')}")
    
    print("\n" + "="*60)


def main():
    """Main execution function."""
    print("\n🔄 Fetching Oura data...")
    
    client = OuraClient()
    
    # Core data
    readiness_data = fetch_readiness_data(client)
    sleep_data = fetch_sleep_data(client)
    activity_data = fetch_activity_data(client)
    
    # Extended data
    stress_data = fetch_stress_data(client)
    workout_data = fetch_workout_data(client)
    hrv_data = fetch_hrv_data(client)
    
    if not any([readiness_data, sleep_data, activity_data]):
        print("✗ Failed to fetch any Oura data")
        sys.exit(1)
    
    now = datetime.now(timezone.utc)
    output_data = {
        "date": now.strftime("%Y-%m-%d"),
        "timestamp": now.isoformat(),
        "oura": {}
    }
    
    if readiness_data:
        output_data["oura"]["readiness"] = readiness_data
    if sleep_data:
        output_data["oura"]["sleep"] = sleep_data
    if activity_data:
        output_data["oura"]["activity"] = activity_data
    if stress_data:
        output_data["oura"]["stress"] = stress_data
    if workout_data:
        output_data["oura"]["workouts"] = workout_data
    if hrv_data:
        output_data["oura"]["hrv"] = hrv_data
    
    output_file = "data/oura_daily.json"
    try:
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"✓ Data saved to: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"✗ Error saving JSON file: {e}")
        sys.exit(1)
    
    print_summary(output_data)
    
    print(f"\n✓ Fetch completed at: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("="*60 + "\n")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
