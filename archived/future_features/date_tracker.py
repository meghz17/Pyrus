"""
Date Night Tracker System
A comprehensive system for tracking date nights with SQLite database and full CRUD operations.
"""

import sqlite3
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta, timezone
import os


def init_database(db_path: str = "/tmp/dates.db") -> None:
    """
    Initialize the database with schema.
    
    Args:
        db_path: Path to the SQLite database file
        
    Raises:
        sqlite3.Error: If database initialization fails
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_timestamp TEXT NOT NULL,
                type TEXT,
                location TEXT,
                description TEXT,
                rating INTEGER CHECK(rating >= 1 AND rating <= 10),
                cost_range TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        print(f"✓ Database initialized at {db_path}")
        
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to initialize database: {e}")


def add_date(date_info: Dict[str, Any], db_path: str = "/tmp/dates.db") -> int:
    """
    Add a new date to the database.
    
    Args:
        date_info: Dictionary containing date information
        db_path: Path to the SQLite database file
        
    Returns:
        The ID of the newly created date record
        
    Raises:
        ValueError: If required fields are missing
        sqlite3.Error: If database operation fails
    """
    if "date_timestamp" not in date_info:
        raise ValueError("date_timestamp is required")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO dates (date_timestamp, type, location, description, rating, cost_range, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            date_info.get("date_timestamp"),
            date_info.get("type"),
            date_info.get("location"),
            date_info.get("description"),
            date_info.get("rating"),
            date_info.get("cost_range"),
            date_info.get("notes")
        ))
        
        date_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return date_id
        
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to add date: {e}")


def get_last_date(db_path: str = "/tmp/dates.db") -> Optional[Dict[str, Any]]:
    """
    Get the most recent date.
    
    Args:
        db_path: Path to the SQLite database file
        
    Returns:
        Dictionary containing the most recent date, or None if no dates exist
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM dates 
            ORDER BY date_timestamp DESC 
            LIMIT 1
        """)
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
        
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to get last date: {e}")


def get_all_dates(limit: Optional[int] = None, db_path: str = "/tmp/dates.db") -> List[Dict[str, Any]]:
    """
    Get all dates, optionally limited.
    
    Args:
        limit: Maximum number of dates to return (None for all)
        db_path: Path to the SQLite database file
        
    Returns:
        List of dictionaries containing date information
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if limit:
            cursor.execute("""
                SELECT * FROM dates 
                ORDER BY date_timestamp DESC 
                LIMIT ?
            """, (limit,))
        else:
            cursor.execute("""
                SELECT * FROM dates 
                ORDER BY date_timestamp DESC
            """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
        
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to get all dates: {e}")


def get_dates_by_type(date_type: str, db_path: str = "/tmp/dates.db") -> List[Dict[str, Any]]:
    """
    Get dates filtered by type.
    
    Args:
        date_type: The type of date to filter by
        db_path: Path to the SQLite database file
        
    Returns:
        List of dictionaries containing date information
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM dates 
            WHERE type = ? 
            ORDER BY date_timestamp DESC
        """, (date_type,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
        
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to get dates by type: {e}")


def get_date_stats(db_path: str = "/tmp/dates.db") -> Dict[str, Any]:
    """
    Get statistics: total dates, avg rating, days since last, favorite types.
    
    Args:
        db_path: Path to the SQLite database file
        
    Returns:
        Dictionary containing statistics
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get total dates
        cursor.execute("SELECT COUNT(*) FROM dates")
        total_dates = cursor.fetchone()[0]
        
        # Get average rating
        cursor.execute("SELECT AVG(rating) FROM dates WHERE rating IS NOT NULL")
        avg_rating_result = cursor.fetchone()[0]
        avg_rating = round(avg_rating_result, 2) if avg_rating_result else None
        
        conn.close()
        
        # Get days since last date
        days_since = days_since_last_date(db_path)
        
        # Get favorite types
        favorite_types = get_favorite_types(limit=3, db_path=db_path)
        
        return {
            "total_dates": total_dates,
            "avg_rating": avg_rating,
            "days_since_last": days_since,
            "favorite_types": favorite_types
        }
        
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to get date stats: {e}")


def update_date(date_id: int, updates: Dict[str, Any], db_path: str = "/tmp/dates.db") -> bool:
    """
    Update an existing date.
    
    Args:
        date_id: ID of the date to update
        updates: Dictionary containing fields to update
        db_path: Path to the SQLite database file
        
    Returns:
        True if update was successful, False if date not found
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    if not updates:
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Build the UPDATE query dynamically
        valid_fields = ["date_timestamp", "type", "location", "description", "rating", "cost_range", "notes"]
        update_fields = []
        values = []
        
        for field, value in updates.items():
            if field in valid_fields:
                update_fields.append(f"{field} = ?")
                values.append(value)
        
        if not update_fields:
            conn.close()
            return False
        
        values.append(date_id)
        query = f"UPDATE dates SET {', '.join(update_fields)} WHERE id = ?"
        
        cursor.execute(query, values)
        rows_affected = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return rows_affected > 0
        
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to update date: {e}")


def delete_date(date_id: int, db_path: str = "/tmp/dates.db") -> bool:
    """
    Delete a date.
    
    Args:
        date_id: ID of the date to delete
        db_path: Path to the SQLite database file
        
    Returns:
        True if deletion was successful, False if date not found
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM dates WHERE id = ?", (date_id,))
        rows_affected = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return rows_affected > 0
        
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to delete date: {e}")


def days_since_last_date(db_path: str = "/tmp/dates.db") -> Optional[int]:
    """
    Calculate days since last date.
    
    Args:
        db_path: Path to the SQLite database file
        
    Returns:
        Number of days since last date, or None if no dates exist
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    try:
        last_date = get_last_date(db_path)
        
        if not last_date or not last_date.get("date_timestamp"):
            return None
        
        # Parse the date timestamp
        date_str = last_date["date_timestamp"]
        try:
            last_date_dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except ValueError:
            # Try parsing without timezone
            last_date_dt = datetime.fromisoformat(date_str)
        
        # Ensure both datetimes are timezone-aware for comparison
        if last_date_dt.tzinfo is not None:
            # Convert to UTC if timezone-aware
            last_date_dt = last_date_dt.astimezone(timezone.utc)
            now = datetime.now(timezone.utc)
        else:
            # Both naive for comparison
            now = datetime.now()
        
        delta = now - last_date_dt
        
        return delta.days
        
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to calculate days since last date: {e}")


def should_remind(days_threshold: int = 14, db_path: str = "/tmp/dates.db") -> bool:
    """
    Check if it's time to remind about date night.
    
    Args:
        days_threshold: Number of days after which to remind
        db_path: Path to the SQLite database file
        
    Returns:
        True if reminder should be sent, False otherwise
    """
    days_since = days_since_last_date(db_path)
    
    if days_since is None:
        return True  # No dates recorded, should remind
    
    return days_since >= days_threshold


def get_favorite_types(limit: int = 3, db_path: str = "/tmp/dates.db") -> List[Tuple[str, int]]:
    """
    Get most common date types.
    
    Args:
        limit: Maximum number of types to return
        db_path: Path to the SQLite database file
        
    Returns:
        List of tuples containing (type, count)
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM dates 
            WHERE type IS NOT NULL 
            GROUP BY type 
            ORDER BY count DESC 
            LIMIT ?
        """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
        
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to get favorite types: {e}")


def get_highest_rated(limit: int = 5, db_path: str = "/tmp/dates.db") -> List[Dict[str, Any]]:
    """
    Get highest rated dates for inspiration.
    
    Args:
        limit: Maximum number of dates to return
        db_path: Path to the SQLite database file
        
    Returns:
        List of dictionaries containing highest rated dates
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM dates 
            WHERE rating IS NOT NULL 
            ORDER BY rating DESC, date_timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
        
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to get highest rated dates: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("DATE NIGHT TRACKER - EXAMPLE USAGE")
    print("=" * 60)
    
    # Initialize database
    print("\n1. Initializing database...")
    init_database()
    
    # Add some sample dates
    print("\n2. Adding sample dates...")
    
    date_id_1 = add_date({
        "date_timestamp": "2025-10-15T19:00:00",
        "type": "dinner",
        "location": "Italian Restaurant",
        "description": "Romantic dinner",
        "rating": 9,
        "cost_range": "moderate",
        "notes": "Great pasta, good conversation"
    })
    print(f"   ✓ Added date #{date_id_1}")
    
    date_id_2 = add_date({
        "date_timestamp": "2025-09-28T14:00:00",
        "type": "activity",
        "location": "City Park",
        "description": "Picnic and hiking",
        "rating": 8,
        "cost_range": "free",
        "notes": "Beautiful weather, enjoyed nature"
    })
    print(f"   ✓ Added date #{date_id_2}")
    
    date_id_3 = add_date({
        "date_timestamp": "2025-09-10T20:30:00",
        "type": "romantic",
        "location": "Rooftop Bar",
        "description": "Sunset drinks",
        "rating": 10,
        "cost_range": "splurge",
        "notes": "Amazing view, special occasion"
    })
    print(f"   ✓ Added date #{date_id_3}")
    
    date_id_4 = add_date({
        "date_timestamp": "2025-08-22T18:00:00",
        "type": "home",
        "location": "Home",
        "description": "Movie night and homemade dinner",
        "rating": 7,
        "cost_range": "budget",
        "notes": "Cozy night in, watched a classic film"
    })
    print(f"   ✓ Added date #{date_id_4}")
    
    date_id_5 = add_date({
        "date_timestamp": "2025-08-05T10:00:00",
        "type": "adventure",
        "location": "Lake",
        "description": "Kayaking and swimming",
        "rating": 9,
        "cost_range": "moderate",
        "notes": "Fun outdoor activity, great exercise"
    })
    print(f"   ✓ Added date #{date_id_5}")
    
    # Get stats
    print("\n3. Getting statistics...")
    stats = get_date_stats()
    print(f"   Total dates: {stats['total_dates']}")
    print(f"   Average rating: {stats['avg_rating']}/10")
    print(f"   Days since last date: {stats['days_since_last']}")
    print(f"   Favorite types: {', '.join([f'{t[0]} ({t[1]})' for t in stats['favorite_types']])}")
    
    # Get last date
    print("\n4. Getting most recent date...")
    last_date = get_last_date()
    if last_date:
        print(f"   Location: {last_date['location']}")
        print(f"   Type: {last_date['type']}")
        print(f"   Rating: {last_date['rating']}/10")
    
    # Get highest rated dates
    print("\n5. Getting highest rated dates...")
    highest = get_highest_rated(limit=3)
    for i, date in enumerate(highest, 1):
        print(f"   #{i}: {date['location']} - {date['rating']}/10")
    
    # Get dates by type
    print("\n6. Getting 'dinner' type dates...")
    dinner_dates = get_dates_by_type("dinner")
    print(f"   Found {len(dinner_dates)} dinner date(s)")
    
    # Update a date
    print("\n7. Updating a date...")
    success = update_date(date_id_1, {
        "notes": "Great pasta, good conversation, will return!",
        "rating": 10
    })
    print(f"   Update successful: {success}")
    
    # Check reminder
    print("\n8. Checking if reminder needed...")
    needs_reminder = should_remind(days_threshold=7)
    print(f"   Should remind (7-day threshold): {needs_reminder}")
    
    # Get all dates
    print("\n9. Getting all dates (limited to 3)...")
    all_dates = get_all_dates(limit=3)
    print(f"   Retrieved {len(all_dates)} date(s)")
    
    # Delete a date (optional - commented out to keep data)
    # print("\n10. Deleting a date...")
    # deleted = delete_date(date_id_4)
    # print(f"   Delete successful: {deleted}")
    
    print("\n" + "=" * 60)
    print("✓ Example completed successfully!")
    print("=" * 60)
