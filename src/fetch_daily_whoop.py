#!/usr/bin/env python3
"""
Daily Whoop Data Fetcher for MagicMirror Integration

This script fetches the latest Whoop health metrics (recovery, sleep, and strain)
and saves them to a JSON file suitable for use with MagicMirror modules.

USAGE:
    python fetch_daily_whoop.py
    ./fetch_daily_whoop.py  (if made executable with chmod +x)

CRON SCHEDULING:
    # Fetch Whoop data every morning at 8:00 AM
    0 8 * * * /usr/bin/python3 /path/to/fetch_daily_whoop.py

    # Fetch multiple times per day
    0 8,14,20 * * * /usr/bin/python3 /path/to/fetch_daily_whoop.py

REQUIREMENTS:
    - WHOOP_CLIENT_ID and WHOOP_CLIENT_SECRET environment variables
    - Active Whoop account with authorized API access
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from whoop_client import WhoopClient


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


def fetch_recovery_data(client: WhoopClient) -> Optional[Dict[str, Any]]:
    """Fetch the latest recovery data."""
    try:
        recovery = client.get_recovery(limit=1)
        if not recovery.get('records'):
            print("⚠ No recovery data available")
            return None
        
        r = recovery['records'][0]
        score_data = r.get('score', {})
        
        return {
            "score": safe_get(score_data, 'recovery_score'),
            "resting_hr": safe_get(score_data, 'resting_heart_rate'),
            "hrv": safe_get(score_data, 'hrv_rmssd_milli'),
            "spo2": safe_get(score_data, 'spo2_percentage'),
            "skin_temp": safe_get(score_data, 'skin_temp_celsius')
        }
    except Exception as e:
        print(f"✗ Error fetching recovery data: {e}")
        return None


def fetch_body_data(client: WhoopClient) -> Optional[Dict[str, Any]]:
    """Fetch user body measurements (height, weight, max HR)."""
    try:
        body = client.get_body_measurements()
        return {
            "height_meter": body.get("height_meter"),
            "weight_kg": body.get("weight_kilogram"),
            "max_hr": body.get("max_heart_rate")
        }
    except Exception as e:
        print(f"⚠ Could not fetch body measurements: {e}")
        return None


def fetch_sleep_data(client: WhoopClient) -> Optional[Dict[str, Any]]:
    """Fetch the latest sleep data."""
    try:
        sleep = client.get_sleep(limit=1)
        if not sleep.get('records'):
            print("⚠ No sleep data available")
            return None
        
        s = sleep['records'][0]
        score_data = s.get('score', {})
        stages = score_data.get('stage_summary', {})
        
        # Convert milliseconds to hours
        total_in_bed = safe_get(stages, 'total_in_bed_time_milli', default=0) / 1000 / 60 / 60
        total_awake = safe_get(stages, 'total_awake_time_milli', default=0) / 1000 / 60 / 60
        rem_hours = safe_get(stages, 'total_rem_sleep_time_milli', default=0) / 1000 / 60 / 60
        deep_hours = safe_get(stages, 'total_slow_wave_sleep_time_milli', default=0) / 1000 / 60 / 60
        light_hours = safe_get(stages, 'total_light_sleep_time_milli', default=0) / 1000 / 60 / 60
        
        return {
            "hours": round(total_in_bed, 2) if total_in_bed else None,
            "performance": safe_get(score_data, 'sleep_performance_percentage'),
            "efficiency": safe_get(score_data, 'sleep_efficiency_percentage'),
            "rem_hours": round(rem_hours, 2) if rem_hours else None,
            "deep_hours": round(deep_hours, 2) if deep_hours else None,
            "light_hours": round(light_hours, 2) if light_hours else None,
            "awake_hours": round(total_awake, 2) if total_awake else None,
            "cycles": safe_get(stages, 'sleep_cycle_count'),
            "respiratory_rate": safe_get(score_data, 'respiratory_rate')
        }
    except Exception as e:
        print(f"✗ Error fetching sleep data: {e}")
        return None


def fetch_strain_data(client: WhoopClient) -> Optional[Dict[str, Any]]:
    """Fetch the latest cycle/strain data."""
    try:
        cycles = client.get_cycles(limit=1)
        if not cycles.get('records'):
            print("⚠ No cycle/strain data available")
            return None
        
        c = cycles['records'][0]
        score_data = c.get('score', {})
        
        # Count workouts in this cycle
        workout_count = 0
        try:
            workouts = client.get_workouts(limit=25)  # Get recent workouts
            if workouts.get('records'):
                cycle_start = c.get('start')
                cycle_end = c.get('end')
                for w in workouts['records']:
                    w_start = w.get('start')
                    if cycle_start and cycle_end and w_start:
                        if cycle_start <= w_start <= cycle_end:
                            workout_count += 1
        except Exception:
            pass  # Non-critical error
        
        return {
            "current": safe_get(score_data, 'strain'),
            "workout_count": workout_count
        }
    except Exception as e:
        print(f"✗ Error fetching strain data: {e}")
        return None


def print_summary(data: Dict[str, Any]) -> None:
    """Print a human-readable summary of the fetched data."""
    print("\n" + "="*60)
    print("📊 WHOOP DATA FETCH SUMMARY")
    print("="*60)
    
    whoop = data.get('whoop', {})
    
    # Recovery
    recovery = whoop.get('recovery', {})
    if recovery:
        print("\n💚 RECOVERY")
        print(f"  Score: {recovery.get('score', 'N/A')}%")
        print(f"  Resting HR: {recovery.get('resting_hr', 'N/A')} bpm")
        print(f"  HRV: {recovery.get('hrv', 'N/A')} ms")
        print(f"  SpO2: {recovery.get('spo2', 'N/A')}%")
        print(f"  Skin Temp: {recovery.get('skin_temp', 'N/A')}°C")
    
    # Sleep
    sleep = whoop.get('sleep', {})
    if sleep:
        print("\n😴 SLEEP")
        print(f"  Total: {sleep.get('hours', 'N/A')} hours")
        print(f"  Performance: {sleep.get('performance', 'N/A')}%")
        print(f"  Efficiency: {sleep.get('efficiency', 'N/A')}%")
        print(f"  REM: {sleep.get('rem_hours', 'N/A')}h | Deep: {sleep.get('deep_hours', 'N/A')}h | Light: {sleep.get('light_hours', 'N/A')}h")
        print(f"  Cycles: {sleep.get('cycles', 'N/A')}")
        print(f"  Respiratory Rate: {sleep.get('respiratory_rate', 'N/A')} breaths/min")
    
    # Strain
    strain = whoop.get('strain', {})
    if strain:
        print("\n🏃 STRAIN")
        print(f"  Current Strain: {strain.get('current', 'N/A')}")
        print(f"  Workouts: {strain.get('workout_count', 'N/A')}")
    
    print("\n" + "="*60)


def main():
    """Main execution function."""
    print("\n🔄 Fetching Whoop data...")
    
    try:
        client = WhoopClient(non_interactive=True)
    except Exception as e:
        print(f"✗ Error initializing Whoop client: {e}")
        sys.exit(1)
    
    # Fetch all data
    recovery_data = fetch_recovery_data(client)
    body_data = fetch_body_data(client)
    sleep_data = fetch_sleep_data(client)
    strain_data = fetch_strain_data(client)
    
    # Check if we got at least some data
    if not any([recovery_data, sleep_data, strain_data]):
        print("✗ Failed to fetch any Whoop data")
        sys.exit(1)
    
    # Build output structure
    now = datetime.now(timezone.utc)
    output_data = {
        "date": now.strftime("%Y-%m-%d"),
        "timestamp": now.isoformat(),
        "whoop": {}
    }
    
    if recovery_data:
        output_data["whoop"]["recovery"] = recovery_data
    if body_data:
        output_data["whoop"]["body"] = body_data
    if sleep_data:
        output_data["whoop"]["sleep"] = sleep_data
    if strain_data:
        output_data["whoop"]["strain"] = strain_data
    
    # Save to JSON file (use absolute path for cron compatibility)
    repo_root = Path(__file__).resolve().parent.parent
    output_dir = repo_root / "data"
    output_file = output_dir / "whoop_daily.json"
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"✓ Data saved to: {output_file}")
    except Exception as e:
        print(f"✗ Error saving JSON file: {e}")
        sys.exit(1)
    
    # Print summary
    print_summary(output_data)
    
    print(f"\n✓ Fetch completed at: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("="*60 + "\n")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
