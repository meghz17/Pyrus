#!/usr/bin/env python3
"""
Friday Date Night Suggester - Smart Thursday-only suggestions for Friday dates

This script is designed to run on THURSDAY ONLY and suggests date ideas for FRIDAY
based on the full week's worth of health data (7-day averages).

DESIGN PHILOSOPHY:
- Friday date nights are weekly tradition
- Suggestions based on weekly health trends, not single-day snapshots
- Only suggests on Thursday to give time to plan
- Uses 14-day threshold to track last date

USAGE:
    python friday_date_suggester.py
    python friday_date_suggester.py --force  # Force run even if not Thursday

CRON SCHEDULING:
    Run every Thursday at 6:00 PM:
    0 18 * * 4 /usr/bin/python3 /path/to/friday_date_suggester.py

INPUT:
    - /tmp/dates.db - Date history database
    - Weekly health data from Whoop and Oura APIs

OUTPUT:
    - friday_date_suggestion.json - Suggestion for MagicMirror display
"""

import os
import json
import sys
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional

# Import modules
from date_tracker import get_last_date, days_since_last_date, init_database
from date_ideas import suggest_based_on_energy
from weekly_health_analyzer import analyze_weekly_health


def is_thursday() -> bool:
    """Check if today is Thursday (weekday 3, where Monday is 0)."""
    return datetime.now().weekday() == 3


def get_next_friday() -> datetime:
    """Calculate the date of the next Friday."""
    today = datetime.now()
    days_until_friday = (4 - today.weekday()) % 7
    
    # If today is Friday, get next Friday (7 days from now)
    if days_until_friday == 0:
        days_until_friday = 7
    
    next_friday = today + timedelta(days=days_until_friday)
    return next_friday.replace(hour=0, minute=0, second=0, microsecond=0)


def should_run(force: bool = False) -> tuple[bool, str]:
    """
    Determine if the suggester should run.
    
    Args:
        force: If True, bypass Thursday check
        
    Returns:
        Tuple of (should_run, reason)
    """
    if force:
        return True, "Force flag enabled"
    
    if not is_thursday():
        day_name = datetime.now().strftime("%A")
        return False, f"Today is {day_name}, not Thursday"
    
    return True, "It's Thursday - time to plan Friday date night!"


def generate_suggestion() -> Dict[str, Any]:
    """Generate Friday date night suggestion based on weekly health data."""
    
    print("\n" + "="*60)
    print("💑 FRIDAY DATE NIGHT SUGGESTER")
    print("="*60)
    
    # Initialize database
    init_database()
    
    # 1. Check last date
    last_date = get_last_date()
    days_since = days_since_last_date()
    
    print(f"\n📅 Days since last date: {days_since if days_since else 'Never'}")
    
    # 2. Analyze weekly health trends
    print("\n📊 Analyzing weekly health trends...")
    weekly_analysis = analyze_weekly_health()
    
    energy_score = weekly_analysis.get("combined_energy_score")
    energy_level = weekly_analysis.get("energy_level", "medium")
    
    print(f"⚡ Weekly energy level: {energy_score}% ({energy_level})")
    
    # 3. Determine if reminder is needed
    reminder_needed = False
    urgency = "none"
    
    if days_since is None:
        reminder_needed = True
        urgency = "first_date"
        message = "No dates recorded yet - time to start your Friday date night tradition! 💕"
    elif days_since >= 14:
        reminder_needed = True
        if days_since >= 21:
            urgency = "urgent"
            message = f"It's been {days_since} days since your last date! Friday is perfect for reconnecting! 🌟"
        else:
            urgency = "moderate"
            message = f"It's been {days_since} days - this Friday would be a great time for date night! ❤️"
    else:
        urgency = "none"
        message = f"You had a date {days_since} days ago. Enjoy the memories, but Friday is always open! 💭"
    
    # 4. Get date suggestions based on weekly energy
    print(f"\n💡 Generating {energy_level}-energy date ideas...")
    
    # Get weekly averages for suggestion - use actual combined score, not defaults
    whoop_recovery = weekly_analysis["whoop_weekly"]["avg_recovery"]
    oura_readiness = weekly_analysis["oura_weekly"]["avg_readiness"]
    
    # Use combined energy score if available, otherwise use whichever is available
    if energy_score:
        suggestions = suggest_based_on_energy(energy_score, energy_score)[:5]
    elif whoop_recovery and oura_readiness:
        suggestions = suggest_based_on_energy(whoop_recovery, oura_readiness)[:5]
    elif whoop_recovery:
        suggestions = suggest_based_on_energy(whoop_recovery, whoop_recovery)[:5]
    elif oura_readiness:
        suggestions = suggest_based_on_energy(oura_readiness, oura_readiness)[:5]
    else:
        # Fallback to medium energy if no data
        suggestions = suggest_based_on_energy(60, 60)[:5]
    
    # 5. Build response
    next_friday = get_next_friday()
    
    suggestion = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "day_of_week": datetime.now().strftime("%A"),
        "is_thursday": is_thursday(),
        "friday_date": {
            "date": next_friday.isoformat(),
            "day_name": "Friday",
            "reminder_needed": reminder_needed,
            "urgency": urgency,
            "message": message
        },
        "last_date": {
            "days_since": days_since,
            "location": last_date.get("location") if last_date else None,
            "date": last_date.get("date_timestamp") if last_date else None,
            "rating": last_date.get("rating") if last_date else None
        },
        "weekly_health": {
            "energy_score": energy_score,
            "energy_level": energy_level,
            "whoop_recovery_avg": weekly_analysis["whoop_weekly"].get("avg_recovery"),
            "whoop_trend": weekly_analysis["whoop_weekly"].get("trend", "unknown"),
            "oura_readiness_avg": weekly_analysis["oura_weekly"].get("avg_readiness"),
            "oura_trend": weekly_analysis["oura_weekly"].get("trend", "unknown"),
            "recommendation": weekly_analysis.get("recommendation", "Unable to generate recommendation")
        },
        "suggested_dates": suggestions
    }
    
    return suggestion


def save_suggestion(suggestion: Dict[str, Any], filename: str = "data/friday_date_suggestion.json"):
    """Save suggestion to JSON file."""
    with open(filename, "w") as f:
        json.dump(suggestion, f, indent=2)
    print(f"\n✓ Suggestion saved to {filename}")


def print_summary(suggestion: Dict[str, Any]):
    """Print formatted summary of the suggestion."""
    print("\n" + "="*60)
    print("📊 FRIDAY DATE NIGHT SUMMARY")
    print("="*60)
    
    friday = suggestion["friday_date"]
    last = suggestion["last_date"]
    health = suggestion["weekly_health"]
    
    print(f"\n📅 Today: {suggestion['day_of_week']}")
    print(f"🗓️  Days since last date: {last['days_since']}")
    print(f"🚨 Urgency: {friday['urgency']}")
    print(f"📢 Reminder needed: {'Yes' if friday['reminder_needed'] else 'No'}")
    
    if last['location']:
        print(f"\n🗓️  Last date:")
        print(f"   Location: {last['location']}")
        print(f"   Rating: {last['rating']}/10")
    
    print(f"\n⚡ Weekly health averages:")
    print(f"   Your recovery: {health['whoop_recovery_avg']}% ({health['whoop_trend']})")
    print(f"   Wife's readiness: {health['oura_readiness_avg']}% ({health['oura_trend']})")
    print(f"   Combined energy: {health['energy_score']}% ({health['energy_level']})")
    
    print(f"\n💡 Top 5 date suggestions for Friday:")
    for i, idea in enumerate(suggestion["suggested_dates"][:5], 1):
        print(f"\n   {i}. {idea['title']}")
        print(f"      {idea['description'][:70]}...")
        print(f"      Budget: {idea['budget']} | Energy: {idea['energy']}")
    
    print(f"\n💬 Message:")
    print(f"   {friday['message']}")
    
    print("\n" + "="*60)


def main():
    """Main execution function."""
    
    # Check for force flag
    force = "--force" in sys.argv or "-f" in sys.argv
    
    # Check if we should run
    should_run_flag, reason = should_run(force)
    
    print("\n" + "="*60)
    print("💑 FRIDAY DATE NIGHT SUGGESTER")
    print("="*60)
    print(f"\n{reason}")
    
    if not should_run_flag:
        print("\n⏸️  Not running - will suggest on Thursday only.")
        print("   Use --force flag to override and test now.\n")
        sys.exit(0)
    
    # Generate suggestion
    suggestion = generate_suggestion()
    
    # Save to file
    save_suggestion(suggestion)
    
    # Print summary
    print_summary(suggestion)
    
    print("\n✓ Friday date suggester completed successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
