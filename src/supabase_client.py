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
