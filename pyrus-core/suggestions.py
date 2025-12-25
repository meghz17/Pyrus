"""
Activity Suggestions Engine
Generates proactive recommendations based on wellness scores
"""
from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy.orm import Session
from models import WellnessScore, ActivitySuggestion


def generate_suggestions(
    date: datetime.date,
    db: Session
) -> Dict:
    """
    Generate activity suggestions for a couple based on wellness scores
    
    Returns:
        {
            "today": {...},
            "upcoming_optimal_days": [...]
        }
    """
    
    # Get today's wellness scores
    partner_a = db.query(WellnessScore).filter(
        WellnessScore.user_id == "partner_a",
        WellnessScore.date == date
    ).first()
    
    partner_b = db.query(WellnessScore).filter(
        WellnessScore.user_id == "partner_b",
        WellnessScore.date == date
    ).first()
    
    if not partner_a or not partner_b:
        return {
            "status": "insufficient_data",
            "message": "Missing wellness scores for today"
        }
    
    # Calculate couple compatibility
    compatibility = _calculate_compatibility(partner_a, partner_b)
    
    # Generate today's suggestions
    today_suggestions = _generate_today_suggestions(
        partner_a.overall_wellness,
        partner_b.overall_wellness,
        compatibility
    )
    
    # Find upcoming optimal days
    optimal_days = _find_optimal_days(date, db)
    
    # Save to database (UPSERT logic)
    existing = db.query(ActivitySuggestion).filter(
        ActivitySuggestion.date == date
    ).first()
    
    if existing:
        # Update existing record
        existing.couple_compatibility = compatibility
        existing.optimal_for_date = today_suggestions["optimal_for_date"]
        existing.optimal_for_workout = today_suggestions["optimal_for_workout"]
        existing.suggestion_type = today_suggestions["type"]
        existing.suggestion_text = today_suggestions["text"]
        existing.confidence = today_suggestions["confidence"]
    else:
        # Insert new record
        suggestion = ActivitySuggestion(
            date=date,
            couple_compatibility=compatibility,
            optimal_for_date=today_suggestions["optimal_for_date"],
            optimal_for_workout=today_suggestions["optimal_for_workout"],
            suggestion_type=today_suggestions["type"],
            suggestion_text=today_suggestions["text"],
            confidence=today_suggestions["confidence"]
        )
        db.add(suggestion)
    
    db.commit()
    
    return {
        "today": {
            "compatibility": compatibility,
            "partner_a_wellness": partner_a.overall_wellness,
            "partner_b_wellness": partner_b.overall_wellness,
            "suggestions": today_suggestions["suggestions"],
            "optimal_for_date": today_suggestions["optimal_for_date"],
            "optimal_for_workout": today_suggestions["optimal_for_workout"]
        },
        "upcoming_optimal_days": optimal_days
    }


def _calculate_compatibility(partner_a: WellnessScore, partner_b: WellnessScore) -> int:
    """
    Calculate couple compatibility score (0-100)
    Higher when both partners have similar wellness levels
    """
    # Average wellness
    avg_wellness = (partner_a.overall_wellness + partner_b.overall_wellness) / 2
    
    # Penalty for large differences
    difference = abs(partner_a.overall_wellness - partner_b.overall_wellness)
    difference_penalty = min(30, difference * 0.5)
    
    compatibility = int(avg_wellness - difference_penalty)
    return max(0, min(100, compatibility))


def _generate_today_suggestions(
    partner_a_wellness: int,
    partner_b_wellness: int,
    compatibility: int
) -> Dict:
    """Generate activity suggestions for today"""
    
    suggestions = []
    optimal_for_date = False
    optimal_for_workout = False
    suggestion_type = "rest"
    confidence = 0
    
    avg_wellness = (partner_a_wellness + partner_b_wellness) / 2
    
    # High compatibility + high wellness = Great for dates
    if compatibility >= 75 and avg_wellness >= 75:
        optimal_for_date = True
        suggestions.append("✨ Perfect day for a date night!")
        suggestions.append("🎯 Both of you are at peak energy")
        suggestion_type = "date"
        confidence = 90
    
    # Both high wellness = Good for workouts
    if partner_a_wellness >= 80 and partner_b_wellness >= 80:
        optimal_for_workout = True
        suggestions.append("💪 Great day for a couples workout!")
        suggestions.append("🏃 Book that gym class you've been eyeing")
        if suggestion_type != "date":
            suggestion_type = "workout"
        confidence = max(confidence, 85)
    
    # Individual high wellness
    if partner_a_wellness >= 80 and partner_b_wellness < 75:
        suggestions.append("🎯 Partner A: Perfect for solo workout")
        suggestion_type = "individual_workout"
        confidence = max(confidence, 75)
    
    if partner_b_wellness >= 80 and partner_a_wellness < 75:
        suggestions.append("🎯 Partner B: Perfect for solo workout")
        suggestion_type = "individual_workout"
        confidence = max(confidence, 75)
    
    # Moderate wellness = Light activities
    if 60 <= avg_wellness < 75:
        suggestions.append("🚶 Good day for light activities")
        suggestions.append("☕ Consider a casual coffee date")
        suggestion_type = "light_activity"
        confidence = max(confidence, 60)
    
    # Low wellness = Rest
    if avg_wellness < 60:
        suggestions.append("😴 Focus on recovery today")
        suggestions.append("🏠 Perfect for a cozy night in")
        suggestion_type = "rest"
        confidence = max(confidence, 70)
    
    # One partner struggling
    if abs(partner_a_wellness - partner_b_wellness) > 20:
        lower_partner = "A" if partner_a_wellness < partner_b_wellness else "B"
        suggestions.append(f"💙 Partner {lower_partner} needs extra support today")
    
    return {
        "suggestions": suggestions,
        "optimal_for_date": optimal_for_date,
        "optimal_for_workout": optimal_for_workout,
        "type": suggestion_type,
        "text": " | ".join(suggestions),
        "confidence": confidence
    }


def _find_optimal_days(current_date: datetime.date, db: Session, days_ahead: int = 7) -> List[Dict]:
    """Find upcoming optimal days based on predicted wellness"""
    
    optimal_days = []
    
    for i in range(1, days_ahead + 1):
        future_date = current_date + timedelta(days=i)
        
        # Get predicted scores (from wellness calculation)
        partner_a = db.query(WellnessScore).filter(
            WellnessScore.user_id == "partner_a",
            WellnessScore.date == current_date
        ).first()
        
        partner_b = db.query(WellnessScore).filter(
            WellnessScore.user_id == "partner_b",
            WellnessScore.date == current_date
        ).first()
        
        if not partner_a or not partner_b:
            continue
        
        # Use predicted scores
        predicted_a = partner_a.predicted_tomorrow
        predicted_b = partner_b.predicted_tomorrow
        
        # If both predicted > 75, it's an optimal day
        if predicted_a >= 75 and predicted_b >= 75:
            optimal_days.append({
                "date": future_date.strftime("%b %d"),
                "partner_a": predicted_a,
                "partner_b": predicted_b,
                "suggestion": "Perfect for date night or active outing"
            })
        elif predicted_a >= 80 or predicted_b >= 80:
            high_partner = "A" if predicted_a > predicted_b else "B"
            optimal_days.append({
                "date": future_date.strftime("%b %d"),
                "partner_a": predicted_a,
                "partner_b": predicted_b,
                "suggestion": f"Good for Partner {high_partner}'s solo activities"
            })
    
    return optimal_days[:3]  # Return top 3 optimal days
