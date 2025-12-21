#!/usr/bin/env python3
"""
Date Night Reminder System - Smart reminder with health-aware suggestions

This script checks if it's time for date night and suggests ideas based on
health data from WHOOP and Oura devices. It integrates with the date tracker
database and health data to provide personalized, energy-appropriate date ideas.

USAGE:
    python date_night_reminder.py
    ./date_night_reminder.py  (if made executable with chmod +x)

CRON SCHEDULING:
    Run this daily to update the reminder JSON for MagicMirror:
    
    # Check for date reminders every morning at 6:00 AM
    0 6 * * * /usr/bin/python3 /path/to/date_night_reminder.py

INPUT FILES:
    - /tmp/dates.db - SQLite database with date history
    - combined_health.json - Unified health data from WHOOP and Oura

OUTPUT FILE:
    - date_reminder.json - Reminder data for MagicMirror display

REQUIREMENTS:
    - Python 3.6+ (uses f-strings and type hints)
    - date_tracker.py module
    - date_ideas.py module
"""

import os
import json
import sys
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Import date tracking functions
from date_tracker import get_last_date, days_since_last_date, init_database
from date_ideas import suggest_based_on_energy


def load_health_data(filename: str = "combined_health.json") -> Optional[Dict[str, Any]]:
    """
    Load combined health data from JSON file.
    
    Args:
        filename: Path to the combined health data file
        
    Returns:
        Dictionary containing health data, or None if loading failed
        
    Handles:
        - Missing files
        - Malformed JSON
        - Permission errors
    """
    if not os.path.exists(filename):
        print(f"⚠ Warning: {filename} not found")
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


def calculate_reminder_urgency(days_since: int) -> str:
    """
    Calculate urgency level based on days since last date.
    
    Args:
        days_since: Number of days since last date
        
    Returns:
        Urgency level: 'none', 'gentle', 'moderate', or 'urgent'
        
    Logic:
        - < 7 days: 'none' (no reminder needed)
        - 7-13 days: 'gentle'
        - 14-20 days: 'moderate'
        - 21+ days: 'urgent'
    """
    if days_since < 7:
        return 'none'
    elif days_since <= 13:
        return 'gentle'
    elif days_since <= 20:
        return 'moderate'
    else:
        return 'urgent'


def get_reminder_message(days_since: int, urgency: str) -> str:
    """
    Generate personalized reminder message based on days and urgency.
    
    Args:
        days_since: Number of days since last date
        urgency: Urgency level ('none', 'gentle', 'moderate', 'urgent')
        
    Returns:
        Personalized reminder message string
    """
    if urgency == 'none':
        return f"You had a date just {days_since} day{'s' if days_since != 1 else ''} ago. Enjoy the memories! 💕"
    elif urgency == 'gentle':
        return f"It's been {days_since} days since your last date night. Maybe start thinking about the next one? 💭"
    elif urgency == 'moderate':
        return f"It's been {days_since} days since your last date night - time to plan something special! ❤️"
    else:  # urgent
        return f"It's been {days_since} days since your last date! Time to reconnect and create new memories! 🌟"


def determine_energy_level(recovery_score: Optional[float], readiness_score: Optional[float]) -> str:
    """
    Determine suggested energy level for date ideas based on health scores.
    
    Args:
        recovery_score: Your WHOOP recovery score (0-100)
        readiness_score: Wife's Oura readiness/activity score (0-100)
        
    Returns:
        Energy level: 'low', 'medium', or 'high'
    """
    scores = []
    if recovery_score is not None:
        scores.append(recovery_score)
    if readiness_score is not None:
        scores.append(readiness_score)
    
    if not scores:
        return 'medium'  # Default if no data
    
    avg_score = sum(scores) / len(scores)
    
    if avg_score >= 70:
        return 'high'
    elif avg_score >= 50:
        return 'medium'
    else:
        return 'low'


def generate_reminder_data(
    db_path: str = "/tmp/dates.db",
    days_threshold: int = 14,
    health_file: str = "combined_health.json"
) -> Dict[str, Any]:
    """
    Main function that generates complete reminder data.
    
    This function orchestrates all the reminder logic:
    1. Checks last date from database
    2. Loads health data
    3. Determines if reminder is needed
    4. Gets energy-based date suggestions
    5. Returns complete reminder data structure
    
    Args:
        db_path: Path to the dates SQLite database
        days_threshold: Number of days before showing reminder (default 14)
        health_file: Path to combined health data JSON
        
    Returns:
        Dictionary containing complete reminder data including:
        - reminder_needed: bool
        - days_since_last_date: int
        - last_date: dict (if exists)
        - urgency: str
        - message: str
        - energy_levels: dict
        - suggested_dates: list
        - timestamp: str
    """
    # Initialize the reminder data structure
    reminder_data = {
        "reminder_needed": False,
        "days_since_last_date": None,
        "last_date": None,
        "urgency": "none",
        "message": "",
        "energy_levels": {
            "your_recovery": None,
            "wife_readiness": None,
            "suggested_energy": "medium"
        },
        "suggested_dates": [],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    # Ensure database exists
    if not os.path.exists(db_path):
        print(f"⚠ Warning: Database not found at {db_path}, initializing...")
        try:
            init_database(db_path)
        except Exception as e:
            print(f"✗ Error initializing database: {e}")
    
    # Get last date from database
    try:
        last_date = get_last_date(db_path)
        days_since = days_since_last_date(db_path)
        
        if last_date:
            # Store simplified last date info
            reminder_data["last_date"] = {
                "timestamp": last_date.get("date_timestamp"),
                "type": last_date.get("type"),
                "location": last_date.get("location"),
                "rating": last_date.get("rating")
            }
        
        if days_since is not None:
            reminder_data["days_since_last_date"] = days_since
            
            # Calculate urgency
            urgency = calculate_reminder_urgency(days_since)
            reminder_data["urgency"] = urgency
            
            # Determine if reminder is needed
            reminder_data["reminder_needed"] = days_since >= days_threshold
            
            # Generate message
            reminder_data["message"] = get_reminder_message(days_since, urgency)
        else:
            # No dates in database
            reminder_data["reminder_needed"] = True
            reminder_data["urgency"] = "urgent"
            reminder_data["message"] = "No date nights recorded yet! Time to start making memories! 💑"
            
    except Exception as e:
        print(f"✗ Error accessing date database: {e}")
        reminder_data["message"] = "Unable to check date history. Consider planning a date soon! 💕"
    
    # Load health data
    health_data = load_health_data(health_file)
    
    if health_data:
        # Extract your WHOOP recovery score
        your_recovery = None
        if 'you' in health_data and 'recovery' in health_data['you']:
            your_recovery = health_data['you']['recovery'].get('score')
            reminder_data["energy_levels"]["your_recovery"] = your_recovery
        
        # Extract wife's Oura readiness score
        # Note: Oura data may have 'readiness' or 'activity' score
        wife_readiness = None
        if 'wife' in health_data:
            wife_data = health_data['wife']
            
            # Try to get readiness score first, fall back to activity score
            if 'readiness' in wife_data:
                wife_readiness = wife_data['readiness'].get('score')
            elif 'activity' in wife_data:
                wife_readiness = wife_data['activity'].get('score')
            
            reminder_data["energy_levels"]["wife_readiness"] = wife_readiness
        
        # Determine suggested energy level
        suggested_energy = determine_energy_level(your_recovery, wife_readiness)
        reminder_data["energy_levels"]["suggested_energy"] = suggested_energy
        
        # Get date suggestions based on energy levels
        try:
            # Use suggest_based_on_energy from date_ideas.py
            suggested_dates = suggest_based_on_energy(
                recovery_score=your_recovery if your_recovery is not None else 50.0,
                readiness_score=wife_readiness
            )
            
            # Limit to 3-5 suggestions
            reminder_data["suggested_dates"] = suggested_dates[:5]
            
        except Exception as e:
            print(f"✗ Error getting date suggestions: {e}")
            reminder_data["suggested_dates"] = []
    else:
        # No health data available - use medium energy default
        print("⚠ No health data available, using default energy level")
        try:
            suggested_dates = suggest_based_on_energy(recovery_score=50.0)
            reminder_data["suggested_dates"] = suggested_dates[:5]
        except Exception as e:
            print(f"✗ Error getting date suggestions: {e}")
            reminder_data["suggested_dates"] = []
    
    return reminder_data


def save_reminder_json(data: Dict[str, Any], filename: str = "date_reminder.json") -> bool:
    """
    Save reminder data to JSON file for MagicMirror display.
    
    Args:
        data: Dictionary containing reminder data
        filename: Output filename (default: date_reminder.json)
        
    Returns:
        True if save successful, False otherwise
        
    Features:
        - Pretty-printed JSON with 2-space indentation
        - Atomic write (temp file then rename)
        - Comprehensive error handling
    """
    try:
        temp_filename = f"{filename}.tmp"
        
        with open(temp_filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Atomic rename
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
    
    Generates reminder data and saves to JSON file.
    Prints a summary of the reminder status.
    
    Exit codes:
        0 - Success
        1 - Error
    """
    print("\n" + "="*60)
    print("💑 DATE NIGHT REMINDER SYSTEM")
    print("="*60)
    
    # Generate reminder data
    reminder = generate_reminder_data()
    
    # Save to JSON file
    output_file = "data/date_reminder.json"
    if not save_reminder_json(reminder, output_file):
        print(f"✗ Failed to save reminder data")
        sys.exit(1)
    
    print(f"✓ Reminder data saved to {output_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 REMINDER SUMMARY")
    print("="*60)
    
    if reminder["days_since_last_date"] is not None:
        print(f"\n📅 Days since last date: {reminder['days_since_last_date']}")
    else:
        print(f"\n📅 No dates recorded yet")
    
    print(f"🚨 Urgency level: {reminder['urgency']}")
    print(f"📢 Reminder needed: {'Yes' if reminder['reminder_needed'] else 'No'}")
    
    if reminder["reminder_needed"]:
        print(f"\n⏰ {reminder['message']}")
    
    # Show last date if available
    if reminder["last_date"]:
        last = reminder["last_date"]
        print(f"\n🗓️  Last date:")
        print(f"   Location: {last.get('location', 'N/A')}")
        print(f"   Type: {last.get('type', 'N/A')}")
        print(f"   Rating: {last.get('rating', 'N/A')}/10")
    
    # Show energy levels
    energy = reminder["energy_levels"]
    print(f"\n⚡ Energy levels:")
    print(f"   Your recovery: {energy['your_recovery']}%" if energy['your_recovery'] else "   Your recovery: N/A")
    print(f"   Wife's readiness: {energy['wife_readiness']}%" if energy['wife_readiness'] else "   Wife's readiness: N/A")
    print(f"   Suggested energy: {energy['suggested_energy']}")
    
    # Show top date suggestions
    if reminder["suggested_dates"]:
        print(f"\n💡 Top date suggestions:")
        for i, idea in enumerate(reminder["suggested_dates"][:3], 1):
            print(f"   {i}. {idea['title']}")
            print(f"      {idea['description'][:70]}...")
            print(f"      Budget: {idea['budget']} | Energy: {idea['energy']}")
    
    print("\n" + "="*60)
    print("✓ Reminder system completed successfully!")
    print("="*60 + "\n")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
