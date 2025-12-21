"""
Sample Health Data Viewer
Shows example data fields available for Pyrus AI assistant
"""

import json
import os


def print_dict_structure(data, prefix="", max_depth=3, current_depth=0):
    """Recursively print dictionary structure with sample values."""
    if current_depth >= max_depth or not isinstance(data, dict):
        return
    
    for key, value in list(data.items())[:10]:  # Limit to first 10 keys
        if isinstance(value, dict):
            print(f"{prefix}{key}: {{...}}")
            if current_depth < max_depth - 1:
                print_dict_structure(value, prefix + "  ", max_depth, current_depth + 1)
        elif isinstance(value, list) and len(value) > 0:
            print(f"{prefix}{key}: [...] ({len(value)} items)")
            if isinstance(value[0], dict):
                print(f"{prefix}  Sample item:")
                print_dict_structure(value[0], prefix + "    ", max_depth, current_depth + 1)
        else:
            # Show actual value for primitive types
            if value is not None and not isinstance(value, (list, dict)):
                value_str = str(value)[:50]
                print(f"{prefix}{key}: {value_str}")


def view_comprehensive_data():
    """View comprehensive health data structure."""
    
    if not os.path.exists("comprehensive_health_data.json"):
        print("Error: comprehensive_health_data.json not found")
        print("Run: python health_data_explorer.py first")
        return
    
    with open("comprehensive_health_data.json", "r") as f:
        data = json.load(f)
    
    print("\n" + "="*60)
    print("🔬 COMPREHENSIVE HEALTH DATA STRUCTURE")
    print("="*60)
    
    print("\n📊 WHOOP DATA FIELDS:")
    print("-" * 60)
    whoop = data.get("whoop", {})
    print_dict_structure(whoop)
    
    print("\n💍 OURA DATA FIELDS:")
    print("-" * 60)
    oura = data.get("oura", {})
    print_dict_structure(oura)
    
    # Show counts
    print("\n" + "="*60)
    print("📈 DATA COUNTS")
    print("="*60)
    
    print("\n🔴 WHOOP:")
    if whoop.get("recovery"):
        print(f"   Recovery records: {len(whoop['recovery'].get('records', []))}")
    if whoop.get("sleep"):
        print(f"   Sleep records: {len(whoop['sleep'].get('records', []))}")
    if whoop.get("workouts"):
        print(f"   Workout records: {len(whoop['workouts'].get('records', []))}")
    
    print("\n💍 OURA:")
    if oura.get("sleep"):
        print(f"   Sleep records: {len(oura['sleep'].get('data', []))}")
    if oura.get("readiness"):
        print(f"   Readiness records: {len(oura['readiness'].get('data', []))}")
    if oura.get("activity"):
        print(f"   Activity records: {len(oura['activity'].get('data', []))}")
    if oura.get("heart_rate"):
        print(f"   Heart rate measurements: {len(oura['heart_rate'].get('data', []))}")
    if oura.get("workouts"):
        print(f"   Workouts: {len(oura['workouts'].get('data', []))}")
    if oura.get("stress"):
        print(f"   Stress records: {len(oura['stress'].get('data', []))}")
    if oura.get("spo2"):
        print(f"   SpO2 records: {len(oura['spo2'].get('data', []))}")
    
    print("\n" + "="*60)


def view_friday_suggestion():
    """View Friday date suggestion structure."""
    
    if not os.path.exists("friday_date_suggestion.json"):
        print("\nError: friday_date_suggestion.json not found")
        print("Run: python friday_date_suggester.py --force first")
        return
    
    with open("friday_date_suggestion.json", "r") as f:
        data = json.load(f)
    
    print("\n" + "="*60)
    print("💑 FRIDAY DATE SUGGESTION DATA")
    print("="*60)
    
    print("\n📅 Friday Date:")
    print(f"   Reminder needed: {data['friday_date']['reminder_needed']}")
    print(f"   Urgency: {data['friday_date']['urgency']}")
    print(f"   Message: {data['friday_date']['message']}")
    
    print("\n⚡ Weekly Health:")
    health = data['weekly_health']
    print(f"   Energy score: {health['energy_score']}%")
    print(f"   Energy level: {health['energy_level']}")
    print(f"   Whoop recovery avg: {health['whoop_recovery_avg']}%")
    print(f"   Oura readiness avg: {health['oura_readiness_avg']}%")
    
    print("\n💡 Suggested Dates:")
    for i, idea in enumerate(data['suggested_dates'][:3], 1):
        print(f"   {i}. {idea['title']} ({idea['energy']} energy, {idea['budget']} budget)")


if __name__ == "__main__":
    view_comprehensive_data()
    view_friday_suggestion()
    
    print("\n" + "="*60)
    print("✓ Data viewing complete")
    print("="*60)
    print("\nAll data is available in JSON files for Pyrus AI assistant:")
    print("  • comprehensive_health_data.json - ALL health metrics")
    print("  • friday_date_suggestion.json - Friday date suggestions")
    print("  • combined_health.json - Current day health summary")
    print("="*60 + "\n")
