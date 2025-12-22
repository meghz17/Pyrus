import os
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

def get_supabase_client():
    # 1. Check os.environ first (GitHub Actions injects secrets here)
    url = os.environ.get("SUPABASE_URL") or os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY") or os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    
    # 2. Fallback: Try loading from .env files for local development
    if not url or not key:
        repo_root = Path(__file__).resolve().parent.parent
        env_path = repo_root / ".env"
        web_env_path = repo_root / "web-dashboard" / ".env"
        
        if env_path.exists():
            load_dotenv(env_path, override=True)
        if web_env_path.exists():
            load_dotenv(web_env_path, override=True)
        
        url = os.environ.get("SUPABASE_URL") or os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY") or os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    
    if not url or not key:
        return None
        
    return create_client(url, key)

def push_health_data(user_data, wife_data, date_suggestion=None):
    """
    Pushes combined health data to Supabase 'health_metrics' table.
    """
    supabase = get_supabase_client()
    if not supabase:
        print("Supabase credentials not found. Skipping cloud sync.")
        return

    data = {
        "user_data": user_data,
        "wife_data": wife_data,
        "date": user_data.get("date") or datetime.now().strftime("%Y-%m-%d"),
    }
    
    if date_suggestion:
        data["date_suggestion"] = date_suggestion
    
    try:
        response = supabase.table("health_metrics").insert(data).execute()
        print("Successfully pushed data to Supabase.")
    except Exception as e:
        print(f"Failed to push to Supabase: {e}")

def get_token(service_name: str):
    """Retrieves a token from the 'tokens' table."""
    supabase = get_supabase_client()
    if not supabase:
        return None
    
    try:
        response = supabase.table("tokens").select("token_data").eq("service_name", service_name).execute()
        if response.data:
            return response.data[0].get("token_data")
    except Exception as e:
        print(f"Error fetching token for {service_name}: {e}")
    return None

def save_token(service_name: str, token_data: dict):
    """Saves or updates a token in the 'tokens' table."""
    supabase = get_supabase_client()
    if not supabase:
        return
    
    try:
        # Upsert: update if service_name exists, else insert
        supabase.table("tokens").upsert({
            "service_name": service_name,
            "token_data": token_data,
            "updated_at": "now()"
        }).execute()
        print(f"Successfully saved {service_name} token to Supabase.")
    except Exception as e:
        print(f"Failed to save token to Supabase: {e}")


# =============================================================================
# Phase J: Individual Metrics Tables
# =============================================================================

def push_whoop_metrics(metrics: dict) -> bool:
    """
    Upserts Whoop metrics to the 'whoop_metrics' table.
    Uses date as unique key for UPSERT behavior.
    """
    supabase = get_supabase_client()
    if not supabase:
        print("Supabase not configured. Skipping whoop_metrics push.")
        return False

    date_str = metrics.get("date") or datetime.now().strftime("%Y-%m-%d")
    
    data = {
        "date": date_str,
        "fetched_at": datetime.now().isoformat(),
        
        # Recovery
        "recovery_score": metrics.get("recovery_score"),
        "resting_hr": metrics.get("resting_hr"),
        "hrv_rmssd": metrics.get("hrv_rmssd"),
        "spo2": metrics.get("spo2"),
        "skin_temp_c": metrics.get("skin_temp_c"),
        
        # Sleep
        "sleep_hours": metrics.get("sleep_hours"),
        "sleep_performance": metrics.get("sleep_performance"),
        "sleep_efficiency": metrics.get("sleep_efficiency"),
        "rem_hours": metrics.get("rem_hours"),
        "deep_hours": metrics.get("deep_hours"),
        "light_hours": metrics.get("light_hours"),
        "awake_hours": metrics.get("awake_hours"),
        "sleep_cycles": metrics.get("sleep_cycles"),
        "respiratory_rate": metrics.get("respiratory_rate"),
        
        # Strain
        "strain_score": metrics.get("strain_score"),
        "workout_count": metrics.get("workout_count"),
        
        # Body
        "height_m": metrics.get("height_m"),
        "weight_kg": metrics.get("weight_kg"),
        "max_hr": metrics.get("max_hr"),
    }
    
    try:
        supabase.table("whoop_metrics").upsert(data, on_conflict="date").execute()
        print(f"✓ Pushed Whoop metrics for {date_str}")
        return True
    except Exception as e:
        print(f"✗ Failed to push whoop_metrics: {e}")
        return False


def push_oura_metrics(metrics: dict) -> bool:
    """
    Upserts Oura metrics to the 'oura_metrics' table.
    Uses date as unique key for UPSERT behavior.
    """
    supabase = get_supabase_client()
    if not supabase:
        print("Supabase not configured. Skipping oura_metrics push.")
        return False

    date_str = metrics.get("date") or datetime.now().strftime("%Y-%m-%d")
    
    data = {
        "date": date_str,
        "fetched_at": datetime.now().isoformat(),
        
        # Readiness
        "readiness_score": metrics.get("readiness_score"),
        "temp_deviation": metrics.get("temp_deviation"),
        "hrv_balance": metrics.get("hrv_balance"),
        
        # Sleep
        "sleep_hours": metrics.get("sleep_hours"),
        "sleep_efficiency": metrics.get("sleep_efficiency"),
        "rem_hours": metrics.get("rem_hours"),
        "deep_hours": metrics.get("deep_hours"),
        "light_hours": metrics.get("light_hours"),
        "awake_hours": metrics.get("awake_hours"),
        "latency_minutes": metrics.get("latency_minutes"),
        "lowest_hr": metrics.get("lowest_hr"),
        "average_hr": metrics.get("average_hr"),
        "average_hrv": metrics.get("average_hrv"),
        
        # Activity
        "activity_score": metrics.get("activity_score"),
        "steps": metrics.get("steps"),
        "active_calories": metrics.get("active_calories"),
        "high_activity_minutes": metrics.get("high_activity_minutes"),
        
        # Stress (Gen3)
        "stress_high": metrics.get("stress_high"),
        "recovery_high": metrics.get("recovery_high"),
        
        # SpO2
        "spo2_avg": metrics.get("spo2_avg"),
    }
    
    try:
        supabase.table("oura_metrics").upsert(data, on_conflict="date").execute()
        print(f"✓ Pushed Oura metrics for {date_str}")
        return True
    except Exception as e:
        print(f"✗ Failed to push oura_metrics: {e}")
        return False
