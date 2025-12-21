#!/usr/bin/env python3
"""
Health Data Combiner for MagicMirror Integration

This script merges WHOOP and Oura Ring daily health metrics into a single unified
JSON file suitable for use with MagicMirror modules. It combines data from
whoop_daily.json and oura_daily.json into combined_health.json.

USAGE:
    python health_combiner.py
    ./health_combiner.py  (if made executable with chmod +x)

CRON SCHEDULING:
    Run this script AFTER the individual data fetchers have run:
    
    # Fetch data and combine every morning at 8:05 AM
    0 8 * * * /usr/bin/python3 /path/to/fetch_daily_whoop.py
    1 8 * * * /usr/bin/python3 /path/to/fetch_daily_oura.py
    5 8 * * * /usr/bin/python3 /path/to/health_combiner.py

INPUT FILES:
    - whoop_daily.json (optional) - WHOOP device data for "you"
    - oura_daily.json (optional) - Oura Ring data for "wife"

OUTPUT FILE:
    - combined_health.json - Unified health data for both users

BEHAVIOR:
    - Gracefully handles missing files (e.g., if one device is offline)
    - Validates JSON structure before merging
    - Uses the most recent timestamp from available data
    - Includes device type in output ("whoop" or "oura")
    - Exit code 0 for success, 1 for error

REQUIREMENTS:
    - At least one input file must exist to generate output
    - Python 3.6+ (uses f-strings and type hints)
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Tuple
from supabase_client import push_health_data


def load_json_safe(filename: str) -> Optional[Dict[str, Any]]:
    """
    Load JSON file with comprehensive error handling.
    
    Args:
        filename: Path to the JSON file to load
        
    Returns:
        Dictionary containing the parsed JSON data, or None if loading failed
        
    Handles:
        - Missing files (returns None silently)
        - Malformed JSON (prints error and returns None)
        - Permission errors (prints error and returns None)
    """
    if not os.path.exists(filename):
        return None
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        print(f"✗ Error: Malformed JSON in {filename}: {e}")
        return None
    except PermissionError:
        print(f"✗ Error: Permission denied reading {filename}")
        return None
    except Exception as e:
        print(f"✗ Error loading {filename}: {e}")
        return None


def merge_health_data(whoop_data: Optional[Dict[str, Any]], 
                     oura_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge WHOOP and Oura data into a unified structure.
    
    Args:
        whoop_data: Dictionary containing WHOOP health metrics (or None)
        oura_data: Dictionary containing Oura Ring metrics (or None)
        
    Returns:
        Dictionary with unified structure mapping:
        - WHOOP data to "you" key
        - Oura data to "wife" key
        - Most recent date and timestamp
        - Device type for each user
        
    Structure:
        {
            "date": "YYYY-MM-DD",
            "timestamp": "ISO-8601",
            "you": {
                "device": "whoop",
                "recovery": {...},
                "sleep": {...},
                "strain": {...}
            },
            "wife": {
                "device": "oura",
                "readiness": {...},
                "sleep": {...},
                "activity": {...}
            }
        }
    """
    combined = {}
    
    dates = []
    timestamps = []
    
    if whoop_data:
        if whoop_data.get('date'):
            dates.append(whoop_data['date'])
        if whoop_data.get('timestamp'):
            timestamps.append(whoop_data['timestamp'])
        
        whoop_metrics = whoop_data.get('whoop', {})
        combined['you'] = {
            "device": "whoop"
        }
        
        if 'recovery' in whoop_metrics:
            combined['you']['recovery'] = whoop_metrics['recovery']
        if 'sleep' in whoop_metrics:
            combined['you']['sleep'] = whoop_metrics['sleep']
        if 'strain' in whoop_metrics:
            combined['you']['strain'] = whoop_metrics['strain']
    
    if oura_data:
        if oura_data.get('date'):
            dates.append(oura_data['date'])
        if oura_data.get('timestamp'):
            timestamps.append(oura_data['timestamp'])
        
        oura_metrics = oura_data.get('oura', {})
        combined['wife'] = {
            "device": "oura"
        }
        
        if 'readiness' in oura_metrics:
            combined['wife']['readiness'] = oura_metrics['readiness']
        if 'sleep' in oura_metrics:
            combined['wife']['sleep'] = oura_metrics['sleep']
        if 'activity' in oura_metrics:
            combined['wife']['activity'] = oura_metrics['activity']
    
    if dates:
        combined['date'] = max(dates)
    else:
        now = datetime.now(timezone.utc)
        combined['date'] = now.strftime("%Y-%m-%d")
    
    if timestamps:
        combined['timestamp'] = max(timestamps)
    else:
        now = datetime.now(timezone.utc)
        combined['timestamp'] = now.isoformat()
    
    result = {
        "date": combined.get('date'),
        "timestamp": combined.get('timestamp')
    }
    
    if 'you' in combined:
        result['you'] = combined['you']
    if 'wife' in combined:
        result['wife'] = combined['wife']
    
    return result


def save_combined_json(data: Dict[str, Any], filename: str) -> bool:
    """
    Save combined health data to JSON file with pretty-printing.
    
    Args:
        data: Dictionary containing the combined health data
        filename: Path to the output file
        
    Returns:
        True if save successful, False otherwise
        
    Features:
        - Pretty-printed JSON with 2-space indentation
        - Atomic write (writes to temp file, then renames)
        - Comprehensive error handling
    """
    try:
        temp_filename = f"{filename}.tmp"
        
        with open(temp_filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        os.replace(temp_filename, filename)
        
        return True
    except PermissionError:
        print(f"✗ Error: Permission denied writing to {filename}")
        return False
    except Exception as e:
        print(f"✗ Error saving {filename}: {e}")
        return False


def main():
    """
    Main execution function.
    """
    print("\n🔄 Combining health data...")
    
    # 1. Define paths (relative to project root)
    repo_root = Path(__file__).resolve().parent.parent
    whoop_file = str(repo_root / "data" / "whoop_daily.json")
    oura_file = str(repo_root / "data" / "oura_daily.json")
    date_file = str(repo_root / "data" / "friday_date_suggestion.json")
    output_file = str(repo_root / "data" / "combined_health.json")
    
    # 2. Load individual data files
    whoop_data = load_json_safe(whoop_file)
    oura_data = load_json_safe(oura_file)
    
    if not whoop_data and not oura_data:
        print("✗ Error: No health data found to combine.")
        sys.exit(1)
        
    # 3. Merge data
    combined_data = merge_health_data(whoop_data, oura_data)
    
    # 4. Save combined JSON locally
    if save_combined_json(combined_data, output_file):
        print(f"✓ Combined health data saved to {output_file}")
    else:
        print("✗ Error: Failed to save combined health data.")
        sys.exit(1)
    
    # 5. Push to Supabase (Cloud Sync)
    print("\n☁️ Syncing to Supabase...")
    date_suggestion = load_json_safe(date_file)
    
    # Use the 'whoop' or 'oura' keys from the individual data files if they exist
    # Supabase push_health_data expects the raw metric objects
    sync_whoop = whoop_data.get('whoop', {}) if whoop_data else {}
    sync_oura = oura_data.get('oura', {}) if oura_data else {}
    
    push_health_data(
        user_data=sync_whoop,
        wife_data=sync_oura,
        date_suggestion=date_suggestion
    )
    
    # 6. Print summary
    print("\n" + "="*60)
    print("📊 COMBINED DATA SUMMARY")
    print("="*60)
    
    if 'you' in combined_data:
        you_data = combined_data['you']
        device = you_data.get('device', 'unknown')
        print(f"\n👤 YOU ({device.upper()})")
        
        if 'recovery' in you_data:
            recovery = you_data['recovery']
            score = recovery.get('score', 'N/A')
            print(f"  Recovery Score: {score}%")
        
        if 'sleep' in you_data:
            sleep = you_data['sleep']
            hours = sleep.get('hours', 'N/A')
            performance = sleep.get('performance', 'N/A')
            print(f"  Sleep: {hours}h (Performance: {performance}%)")
        
        if 'strain' in you_data:
            strain = you_data['strain']
            current = strain.get('current', 'N/A')
            print(f"  Strain: {current}")
    
    if 'wife' in combined_data:
        wife_data = combined_data['wife']
        device = wife_data.get('device', 'unknown')
        print(f"\n👤 MEGHNA ({device.upper()})")
        
        if 'readiness' in wife_data:
            readiness = wife_data['readiness']
            score = readiness.get('score', 'N/A')
            print(f"  Readiness Score: {score}%")
        
        if 'sleep' in wife_data:
            sleep = wife_data['sleep']
            score = sleep.get('score', 'N/A')
            total = sleep.get('total_hours', 'N/A')
            print(f"  Sleep Score: {score}% (Total: {total}h)")
        
        if 'activity' in wife_data:
            activity = wife_data['activity']
            score = activity.get('score', 'N/A')
            steps = activity.get('steps', 'N/A')
            print(f"  Activity Score: {score}% (Steps: {steps})")
    
    print("\n" + "="*60)
    print(f"✓ Combination completed at: {combined_data.get('timestamp', 'unknown')}")
    print("="*60 + "\n")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
