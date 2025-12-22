"""
Weekly Health Analyzer
Analyzes the past 7 days of health data from both partners to provide
intelligent date night suggestions based on weekly trends, not just current day.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from whoop_client import WhoopClient
from oura_client import OuraClient

load_dotenv()


def get_weekly_whoop_data(days=7) -> Dict[str, Any]:
    """Fetch last 7 days of Whoop recovery data and calculate averages."""
    client = WhoopClient(
        client_id=os.getenv("WHOOP_CLIENT_ID"),
        client_secret=os.getenv("WHOOP_CLIENT_SECRET")
    )
    
    try:
        # Fetch recent recovery data (limit to last 7 records instead of date range)
        recovery_data = client.get_recovery(limit=days)
        records = recovery_data.get("records", [])
        
        if not records:
            return {
                "days_analyzed": 0,
                "avg_recovery": None,
                "avg_hrv": None,
                "avg_rhr": None,
                "trend": "insufficient_data"
            }
        
        # Calculate averages
        recovery_scores = []
        hrv_values = []
        rhr_values = []
        
        for record in records:
            score = record.get("score", {})
            recovery_score = score.get("recovery_score")
            hrv = score.get("hrv_rmssd_milli")
            rhr = score.get("resting_heart_rate")
            
            if recovery_score is not None:
                recovery_scores.append(recovery_score)
            if hrv is not None:
                hrv_values.append(hrv)
            if rhr is not None:
                rhr_values.append(rhr)
        
        avg_recovery = sum(recovery_scores) / len(recovery_scores) if recovery_scores else None
        avg_hrv = sum(hrv_values) / len(hrv_values) if hrv_values else None
        avg_rhr = sum(rhr_values) / len(rhr_values) if rhr_values else None
        
        # Determine trend (last 3 days vs previous 4 days)
        trend = "stable"
        if len(recovery_scores) >= 7:
            recent_avg = sum(recovery_scores[:3]) / 3
            older_avg = sum(recovery_scores[3:7]) / 4
            if recent_avg > older_avg + 5:
                trend = "improving"
            elif recent_avg < older_avg - 5:
                trend = "declining"
        
        return {
            "days_analyzed": len(records),
            "avg_recovery": round(avg_recovery, 1) if avg_recovery else None,
            "avg_hrv": round(avg_hrv, 1) if avg_hrv else None,
            "avg_rhr": round(avg_rhr, 1) if avg_rhr else None,
            "trend": trend,
            "raw_data": records[:7]  # Keep last 7 for reference
        }
        
    except Exception as e:
        print(f"Error fetching Whoop weekly data: {e}")
        return {
            "days_analyzed": 0,
            "avg_recovery": None,
            "error": str(e)
        }


def get_weekly_oura_data(days=7) -> Dict[str, Any]:
    """Fetch last 7 days of Oura readiness/activity data and calculate averages."""
    client = OuraClient(access_token=os.getenv("OURA_ACCESS_TOKEN"))
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    try:
        readiness_data = client.get_daily_readiness(start_date=start_str, end_date=end_str)
        activity_data = client.get_daily_activity(start_date=start_str, end_date=end_str)
        
        readiness_records = readiness_data.get("data", [])
        activity_records = activity_data.get("data", [])
        
        if not readiness_records:
            return {
                "days_analyzed": 0,
                "avg_readiness": None,
                "avg_activity": None,
                "trend": "insufficient_data"
            }
        
        # Calculate averages
        readiness_scores = [r.get("score") for r in readiness_records if r.get("score")]
        activity_scores = [a.get("score") for a in activity_records if a.get("score")]
        
        avg_readiness = sum(readiness_scores) / len(readiness_scores) if readiness_scores else None
        avg_activity = sum(activity_scores) / len(activity_scores) if activity_scores else None
        
        # Determine trend
        trend = "stable"
        if len(readiness_scores) >= 7:
            recent_avg = sum(readiness_scores[:3]) / 3
            older_avg = sum(readiness_scores[3:7]) / 4
            if recent_avg > older_avg + 5:
                trend = "improving"
            elif recent_avg < older_avg - 5:
                trend = "declining"
        
        return {
            "days_analyzed": len(readiness_records),
            "avg_readiness": round(avg_readiness, 1) if avg_readiness else None,
            "avg_activity": round(avg_activity, 1) if avg_activity else None,
            "trend": trend,
            "raw_data": {
                "readiness": readiness_records[:7],
                "activity": activity_records[:7]
            }
        }
        
    except Exception as e:
        print(f"Error fetching Oura weekly data: {e}")
        return {
            "days_analyzed": 0,
            "avg_readiness": None,
            "error": str(e)
        }


def analyze_weekly_health() -> Dict[str, Any]:
    """Analyze both partners' health data for the week and provide recommendations."""
    print("Analyzing weekly health trends...")
    
    whoop = get_weekly_whoop_data()
    oura = get_weekly_oura_data()
    
    # Calculate combined energy level
    avg_recovery = whoop.get("avg_recovery")
    avg_readiness = oura.get("avg_readiness")
    
    if avg_recovery and avg_readiness:
        combined_energy = (avg_recovery + avg_readiness) / 2
    elif avg_recovery:
        combined_energy = avg_recovery
    elif avg_readiness:
        combined_energy = avg_readiness
    else:
        combined_energy = None
    
    # Determine energy level category
    if combined_energy:
        if combined_energy >= 70:
            energy_level = "high"
            recommendation = "You both have great energy! Perfect for active or adventurous dates."
        elif combined_energy >= 50:
            energy_level = "medium"
            recommendation = "Moderate energy levels. Great for cultural activities, dining, or light activities."
        else:
            energy_level = "low"
            recommendation = "Lower energy this week. Consider relaxing, cozy, or restorative activities."
    else:
        energy_level = "unknown"
        recommendation = "Unable to determine energy levels from health data."
    
    analysis = {
        "timestamp": datetime.utcnow().isoformat(),
        "week_analyzed": f"{(datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d')} to {datetime.utcnow().strftime('%Y-%m-%d')}",
        "whoop_weekly": whoop,
        "oura_weekly": oura,
        "combined_energy_score": round(combined_energy, 1) if combined_energy else None,
        "energy_level": energy_level,
        "recommendation": recommendation,
        "both_trends_aligned": whoop.get("trend") == oura.get("trend")
    }
    
    return analysis


def save_weekly_analysis(filename="data/weekly_health_analysis.json"):
    """Analyze and save weekly health data."""
    analysis = analyze_weekly_health()
    
    with open(filename, "w") as f:
        json.dump(analysis, f, indent=2)
    
    print(f"✓ Weekly analysis saved to {filename}")
    return analysis


if __name__ == "__main__":
    print("\n" + "="*60)
    print("📊 WEEKLY HEALTH ANALYZER")
    print("="*60)
    
    analysis = save_weekly_analysis()
    
    print("\n" + "="*60)
    print("WEEKLY SUMMARY")
    print("="*60)
    print(f"\n📅 Period: {analysis['week_analyzed']}")
    print(f"\n🔴 Your (Whoop) weekly average:")
    print(f"   Recovery: {analysis['whoop_weekly']['avg_recovery']}%")
    print(f"   HRV: {analysis['whoop_weekly']['avg_hrv']}ms")
    print(f"   Trend: {analysis['whoop_weekly']['trend']}")
    
    print(f"\n💍 Wife's (Oura) weekly average:")
    print(f"   Readiness: {analysis['oura_weekly']['avg_readiness']}%")
    print(f"   Activity: {analysis['oura_weekly']['avg_activity']}%")
    print(f"   Trend: {analysis['oura_weekly']['trend']}")
    
    print(f"\n⚡ Combined Energy: {analysis['combined_energy_score']}% ({analysis['energy_level']})")
    print(f"\n💡 Recommendation:")
    print(f"   {analysis['recommendation']}")
    print("\n" + "="*60 + "\n")
