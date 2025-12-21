import os
from dotenv import load_dotenv
from whoop_client import WhoopClient
import json

load_dotenv()

client_id = os.getenv("WHOOP_CLIENT_ID")
client_secret = os.getenv("WHOOP_CLIENT_SECRET")
redirect_uri = os.getenv("WHOOP_REDIRECT_URI", "https://localhost/callback")

if not client_id or not client_secret:
    print("\n" + "="*60)
    print("ERROR: Missing Whoop API Credentials")
    print("="*60)
    print("\nPlease follow these steps:")
    print("1. Go to https://developer.whoop.com/")
    print("2. Create an application to get your Client ID and Secret")
    print("3. Copy .env.example to .env")
    print("4. Add your credentials to the .env file")
    print("\nRequired variables:")
    print("  - WHOOP_CLIENT_ID")
    print("  - WHOOP_CLIENT_SECRET")
    print("  - WHOOP_REDIRECT_URI (optional, defaults to https://localhost/callback)")
    print("\n" + "="*60 + "\n")
    exit(1)

def print_section(title: str):
    print("\n" + "="*60)
    print(f"{title}")
    print("="*60 + "\n")

def main():
    print("\n🏃 Whoop API Client Example")
    
    client = WhoopClient(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri
    )
    
    try:
        print_section("1. USER PROFILE")
        profile = client.get_profile()
        print(json.dumps(profile, indent=2))
        
        print_section("2. BODY MEASUREMENTS")
        body = client.get_body_measurements()
        print(json.dumps(body, indent=2))
        
        print_section("3. LATEST RECOVERY DATA (Last 3)")
        recovery = client.get_recovery(limit=3)
        print(json.dumps(recovery, indent=2))
        
        print_section("4. LATEST SLEEP DATA (Last 3)")
        sleep = client.get_sleep(limit=3)
        print(json.dumps(sleep, indent=2))
        
        print_section("5. LATEST WORKOUTS (Last 3)")
        workouts = client.get_workouts(limit=3)
        print(json.dumps(workouts, indent=2))
        
        print_section("6. LATEST CYCLES (Last 3)")
        cycles = client.get_cycles(limit=3)
        print(json.dumps(cycles, indent=2))
        
        if cycles.get("records") and len(cycles["records"]) > 0:
            first_cycle = cycles["records"][0]
            cycle_id = first_cycle.get("id")
            
            if cycle_id:
                print_section(f"7. RECOVERY FOR CYCLE {cycle_id}")
                cycle_recovery = client.get_recovery_for_cycle(cycle_id)
                print(json.dumps(cycle_recovery, indent=2))
                
                print_section(f"8. SLEEP FOR CYCLE {cycle_id}")
                cycle_sleep = client.get_sleep_for_cycle(cycle_id)
                print(json.dumps(cycle_sleep, indent=2))
        
        print_section("✓ SUCCESS")
        print("All API calls completed successfully!")
        print("\nYour Whoop data has been retrieved.")
        print("Token saved in whoop_tokens.json for future use.\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        raise

if __name__ == "__main__":
    main()
