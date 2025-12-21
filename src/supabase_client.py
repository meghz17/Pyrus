import os
from supabase import create_client, Client

def get_supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
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
