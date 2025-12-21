"""
Comprehensive Health Data Explorer
Fetches ALL available data from both Whoop and Oura APIs for maximum visibility.
"""

import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from whoop_client import WhoopClient
from oura_client import OuraClient

load_dotenv()


def fetch_all_whoop_data(days_back=7):
    """Fetch maximum data from Whoop API."""
    print("\n" + "="*60)
    print("🔴 FETCHING ALL WHOOP DATA")
    print("="*60)
    
    client = WhoopClient(
        client_id=os.getenv("WHOOP_CLIENT_ID"),
        client_secret=os.getenv("WHOOP_CLIENT_SECRET")
    )
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days_back)
    start_str = start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end_str = end_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    
    data = {}
    
    # 1. User Profile
    try:
        print("\n📊 Fetching user profile...")
        data["profile"] = client.get_profile()
        print(f"   ✓ Profile: {data['profile'].get('first_name', 'N/A')} {data['profile'].get('last_name', 'N/A')}")
    except Exception as e:
        print(f"   ✗ Profile failed: {e}")
        data["profile"] = None
    
    # 2. Body Measurements
    try:
        print("\n📏 Fetching body measurements...")
        data["body_measurements"] = client.get_body_measurements()
        body = data["body_measurements"]
        print(f"   ✓ Height: {body.get('height_meter', 'N/A')}m")
        print(f"   ✓ Weight: {body.get('weight_kilogram', 'N/A')}kg")
        print(f"   ✓ Max HR: {body.get('max_heart_rate', 'N/A')} bpm")
    except Exception as e:
        print(f"   ✗ Body measurements failed: {e}")
        data["body_measurements"] = None
    
    # 3. Cycles (last 7 days worth)
    try:
        print(f"\n🔄 Fetching cycles ({days_back} days)...")
        data["cycles"] = client.get_cycles(start=start_str, end=end_str, limit=50)
        cycles_count = len(data["cycles"].get("records", []))
        print(f"   ✓ Found {cycles_count} cycles")
        
        # Get detailed cycle data for each cycle
        data["cycles_detailed"] = []
        for cycle in data["cycles"].get("records", [])[:5]:  # Last 5 for detail
            cycle_id = cycle.get("id")
            try:
                detailed = client.get_cycle_by_id(cycle_id)
                data["cycles_detailed"].append(detailed)
            except:
                pass
        print(f"   ✓ Fetched {len(data['cycles_detailed'])} detailed cycles")
        
    except Exception as e:
        print(f"   ✗ Cycles failed: {e}")
        data["cycles"] = None
        data["cycles_detailed"] = []
    
    # 4. Recovery Data
    try:
        print(f"\n💚 Fetching recovery data ({days_back} days)...")
        data["recovery"] = client.get_recovery(start=start_str, end=end_str, limit=50)
        recovery_count = len(data["recovery"].get("records", []))
        print(f"   ✓ Found {recovery_count} recovery records")
        
        # Show latest recovery
        if recovery_count > 0:
            latest = data["recovery"]["records"][0]
            print(f"   ✓ Latest recovery: {latest.get('score', {}).get('recovery_score', 'N/A')}%")
            print(f"   ✓ HRV: {latest.get('score', {}).get('hrv_rmssd_milli', 'N/A')}ms")
            print(f"   ✓ RHR: {latest.get('score', {}).get('resting_heart_rate', 'N/A')} bpm")
    except Exception as e:
        print(f"   ✗ Recovery failed: {e}")
        data["recovery"] = None
    
    # 5. Sleep Data
    try:
        print(f"\n😴 Fetching sleep data ({days_back} days)...")
        data["sleep"] = client.get_sleep(start=start_str, end=end_str, limit=50)
        sleep_count = len(data["sleep"].get("records", []))
        print(f"   ✓ Found {sleep_count} sleep records")
        
        # Get detailed sleep for last 3 sleeps
        data["sleep_detailed"] = []
        for sleep in data["sleep"].get("records", [])[:3]:
            sleep_id = sleep.get("id")
            try:
                detailed = client.get_sleep_by_id(sleep_id)
                data["sleep_detailed"].append(detailed)
            except:
                pass
        print(f"   ✓ Fetched {len(data['sleep_detailed'])} detailed sleep records")
        
        # Show latest sleep
        if sleep_count > 0:
            latest = data["sleep"]["records"][0]
            score = latest.get("score", {})
            print(f"   ✓ Latest sleep score: {score.get('sleep_performance_percentage', 'N/A')}%")
            print(f"   ✓ Duration: {score.get('total_sleep_duration_milli', 0) / 1000 / 60:.0f} min")
    except Exception as e:
        print(f"   ✗ Sleep failed: {e}")
        data["sleep"] = None
        data["sleep_detailed"] = []
    
    # 6. Workout Data
    try:
        print(f"\n🏋️ Fetching workout data ({days_back} days)...")
        data["workouts"] = client.get_workouts(start=start_str, end=end_str, limit=50)
        workout_count = len(data["workouts"].get("records", []))
        print(f"   ✓ Found {workout_count} workout records")
        
        # Get detailed workouts
        data["workouts_detailed"] = []
        for workout in data["workouts"].get("records", [])[:5]:
            workout_id = workout.get("id")
            try:
                detailed = client.get_workout_by_id(workout_id)
                data["workouts_detailed"].append(detailed)
            except:
                pass
        print(f"   ✓ Fetched {len(data['workouts_detailed'])} detailed workouts")
        
        # Show workout summary
        if workout_count > 0:
            latest = data["workouts"]["records"][0]
            print(f"   ✓ Latest workout: {latest.get('sport_id', 'N/A')}")
            print(f"   ✓ Strain: {latest.get('score', {}).get('strain', 'N/A')}")
    except Exception as e:
        print(f"   ✗ Workouts failed: {e}")
        data["workouts"] = None
        data["workouts_detailed"] = []
    
    return data


def fetch_all_oura_data(days_back=7):
    """Fetch maximum data from Oura API."""
    print("\n" + "="*60)
    print("💍 FETCHING ALL OURA DATA")
    print("="*60)
    
    client = OuraClient(access_token=os.getenv("OURA_ACCESS_TOKEN"))
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days_back)
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    data = {}
    
    # 1. Personal Info
    try:
        print("\n📊 Fetching personal info...")
        data["personal_info"] = client.get_personal_info()
        info = data["personal_info"]
        print(f"   ✓ Age: {info.get('age', 'N/A')}")
        print(f"   ✓ Weight: {info.get('weight', 'N/A')}kg")
        print(f"   ✓ Height: {info.get('height', 'N/A')}m")
    except Exception as e:
        print(f"   ✗ Personal info failed: {e}")
        data["personal_info"] = None
    
    # 2. Sleep Data (detailed)
    try:
        print(f"\n😴 Fetching detailed sleep ({days_back} days)...")
        data["sleep"] = client.get_sleep(start_date=start_str, end_date=end_str)
        sleep_count = len(data["sleep"].get("data", []))
        print(f"   ✓ Found {sleep_count} sleep records")
        if sleep_count > 0:
            latest = data["sleep"]["data"][0]
            print(f"   ✓ Latest duration: {latest.get('total_sleep_duration', 0) / 3600:.1f}h")
            print(f"   ✓ Efficiency: {latest.get('efficiency', 'N/A')}%")
    except Exception as e:
        print(f"   ✗ Sleep failed: {e}")
        data["sleep"] = None
    
    # 3. Daily Sleep (scores)
    try:
        print(f"\n😴 Fetching daily sleep scores ({days_back} days)...")
        data["daily_sleep"] = client.get_daily_sleep(start_date=start_str, end_date=end_str)
        print(f"   ✓ Found {len(data['daily_sleep'].get('data', []))} daily sleep scores")
    except Exception as e:
        print(f"   ✗ Daily sleep failed: {e}")
        data["daily_sleep"] = None
    
    # 4. Daily Readiness
    try:
        print(f"\n💪 Fetching daily readiness ({days_back} days)...")
        data["readiness"] = client.get_daily_readiness(start_date=start_str, end_date=end_str)
        readiness_count = len(data["readiness"].get("data", []))
        print(f"   ✓ Found {readiness_count} readiness records")
        if readiness_count > 0:
            latest = data["readiness"]["data"][0]
            print(f"   ✓ Latest score: {latest.get('score', 'N/A')}")
    except Exception as e:
        print(f"   ✗ Readiness failed: {e}")
        data["readiness"] = None
    
    # 5. Daily Activity
    try:
        print(f"\n🏃 Fetching daily activity ({days_back} days)...")
        data["activity"] = client.get_daily_activity(start_date=start_str, end_date=end_str)
        activity_count = len(data["activity"].get("data", []))
        print(f"   ✓ Found {activity_count} activity records")
        if activity_count > 0:
            latest = data["activity"]["data"][0]
            print(f"   ✓ Latest score: {latest.get('score', 'N/A')}")
            print(f"   ✓ Steps: {latest.get('steps', 'N/A'):,}")
    except Exception as e:
        print(f"   ✗ Activity failed: {e}")
        data["activity"] = None
    
    # 6. Daily SpO2
    try:
        print(f"\n🫁 Fetching SpO2 data ({days_back} days)...")
        data["spo2"] = client.get_daily_spo2(start_date=start_str, end_date=end_str)
        spo2_count = len(data["spo2"].get("data", []))
        print(f"   ✓ Found {spo2_count} SpO2 records")
        if spo2_count > 0:
            latest = data["spo2"]["data"][0]
            print(f"   ✓ Average SpO2: {latest.get('spo2_percentage', {}).get('average', 'N/A')}%")
    except Exception as e:
        print(f"   ✗ SpO2 failed: {e}")
        data["spo2"] = None
    
    # 7. Heart Rate (NEW)
    try:
        print(f"\n❤️  Fetching heart rate data ({days_back} days)...")
        start_datetime = start_date.strftime("%Y-%m-%dT%H:%M:%S")
        end_datetime = end_date.strftime("%Y-%m-%dT%H:%M:%S")
        data["heart_rate"] = client.get_heart_rate(start_datetime=start_datetime, end_datetime=end_datetime)
        hr_count = len(data["heart_rate"].get("data", []))
        print(f"   ✓ Found {hr_count} heart rate measurements")
    except Exception as e:
        print(f"   ✗ Heart rate failed: {e}")
        data["heart_rate"] = None
    
    # 8. Workouts (NEW)
    try:
        print(f"\n🏋️ Fetching workouts ({days_back} days)...")
        data["workouts"] = client.get_workouts(start_date=start_str, end_date=end_str)
        workout_count = len(data["workouts"].get("data", []))
        print(f"   ✓ Found {workout_count} workouts")
    except Exception as e:
        print(f"   ✗ Workouts failed: {e}")
        data["workouts"] = None
    
    # 9. Daily Stress (NEW)
    try:
        print(f"\n😰 Fetching daily stress ({days_back} days)...")
        data["stress"] = client.get_daily_stress(start_date=start_str, end_date=end_str)
        stress_count = len(data["stress"].get("data", []))
        print(f"   ✓ Found {stress_count} stress records")
    except Exception as e:
        print(f"   ✗ Stress failed: {e}")
        data["stress"] = None
    
    # 10. Tags (NEW)
    try:
        print(f"\n🏷️  Fetching tags ({days_back} days)...")
        data["tags"] = client.get_tags(start_date=start_str, end_date=end_str)
        tags_count = len(data["tags"].get("data", []))
        print(f"   ✓ Found {tags_count} tags")
    except Exception as e:
        print(f"   ✗ Tags failed: {e}")
        data["tags"] = None
    
    # 11. Ring Configuration (NEW)
    try:
        print(f"\n💍 Fetching ring configuration...")
        data["ring_config"] = client.get_ring_configuration()
        print(f"   ✓ Ring configured")
    except Exception as e:
        print(f"   ✗ Ring config failed: {e}")
        data["ring_config"] = None
    
    return data


def save_comprehensive_data(whoop_data, oura_data, filename="data/comprehensive_health_data.json"):
    """Save all data to JSON file."""
    combined = {
        "timestamp": datetime.utcnow().isoformat(),
        "whoop": whoop_data,
        "oura": oura_data
    }
    
    with open(filename, "w") as f:
        json.dump(combined, f, indent=2)
    
    print(f"\n✓ Comprehensive data saved to {filename}")
    return combined


def print_data_summary(data):
    """Print summary of what data is available."""
    print("\n" + "="*60)
    print("📈 DATA SUMMARY")
    print("="*60)
    
    whoop = data.get("whoop", {})
    oura = data.get("oura", {})
    
    print("\n🔴 WHOOP DATA AVAILABLE:")
    whoop_endpoints = {
        "Profile": whoop.get("profile"),
        "Body Measurements": whoop.get("body_measurements"),
        "Cycles": whoop.get("cycles"),
        "Cycles (Detailed)": whoop.get("cycles_detailed"),
        "Recovery": whoop.get("recovery"),
        "Sleep": whoop.get("sleep"),
        "Sleep (Detailed)": whoop.get("sleep_detailed"),
        "Workouts": whoop.get("workouts"),
        "Workouts (Detailed)": whoop.get("workouts_detailed")
    }
    
    for name, data_obj in whoop_endpoints.items():
        status = "✓" if data_obj else "✗"
        if isinstance(data_obj, dict):
            count = len(data_obj.get("records", data_obj.get("data", [])))
            print(f"   {status} {name}: {count} records" if count > 0 else f"   {status} {name}")
        elif isinstance(data_obj, list):
            print(f"   {status} {name}: {len(data_obj)} records")
        else:
            print(f"   {status} {name}")
    
    print("\n💍 OURA DATA AVAILABLE:")
    oura_endpoints = {
        "Personal Info": oura.get("personal_info"),
        "Sleep (Detailed)": oura.get("sleep"),
        "Daily Sleep Scores": oura.get("daily_sleep"),
        "Daily Readiness": oura.get("readiness"),
        "Daily Activity": oura.get("activity"),
        "Daily SpO2": oura.get("spo2"),
        "Heart Rate": oura.get("heart_rate"),
        "Workouts": oura.get("workouts"),
        "Daily Stress": oura.get("stress"),
        "Tags": oura.get("tags"),
        "Ring Configuration": oura.get("ring_config")
    }
    
    for name, data_obj in oura_endpoints.items():
        status = "✓" if data_obj else "✗"
        if isinstance(data_obj, dict) and "data" in data_obj:
            count = len(data_obj["data"])
            print(f"   {status} {name}: {count} records")
        else:
            print(f"   {status} {name}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔬 COMPREHENSIVE HEALTH DATA EXPLORER")
    print("="*60)
    print("\nThis script fetches ALL available data from both APIs.")
    print("Data will be saved to: comprehensive_health_data.json")
    
    days = int(input("\nHow many days of historical data? (default 7): ") or "7")
    
    # Fetch all data
    whoop_data = fetch_all_whoop_data(days_back=days)
    oura_data = fetch_all_oura_data(days_back=days)
    
    # Save to file
    comprehensive = save_comprehensive_data(whoop_data, oura_data)
    
    # Print summary
    print_data_summary(comprehensive)
    
    # Calculate file size
    import os
    file_size = os.path.getsize("comprehensive_health_data.json")
    print(f"\n📦 Total data size: {file_size / 1024:.1f} KB")
    
    print("\n" + "="*60)
    print("✓ EXPLORATION COMPLETE")
    print("="*60)
    print("\nYou can now inspect 'comprehensive_health_data.json' to see")
    print("all available data fields for Pyrus (your AI assistant).")
    print("="*60 + "\n")
