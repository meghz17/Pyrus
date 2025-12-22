#!/usr/bin/env python3
"""
Pyrus AI Health Coach - GPT-4 powered health coaching

This script provides AI-powered health coaching based on comprehensive health data
from Whoop and Oura wearables. Uses OpenAI's GPT-4 via Replit AI Integrations.

Features:
- Personalized health insights
- Weekly trend analysis
- Relationship-aware date recommendations
- Natural conversation interface

Usage:
    python pyrus_ai_coach.py --query "How's my recovery today?"
    python pyrus_ai_coach.py --daily-summary
"""

import os
import json
import sys
import argparse
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

class PyrusAICoach:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(
            base_url=os.getenv("AI_INTEGRATIONS_OPENAI_BASE_URL"),
            api_key=os.getenv("AI_INTEGRATIONS_OPENAI_API_KEY")
        )
        self.model = "gpt-4o"
        
    def load_health_data(self):
        """Load all available health data"""
        data = {}
        
        try:
            with open("data/combined_health.json", "r") as f:
                data["current"] = json.load(f)
        except:
            data["current"] = None
            
        try:
            with open("data/weekly_health_analysis.json", "r") as f:
                data["weekly"] = json.load(f)
        except:
            data["weekly"] = None
            
        try:
            with open("data/friday_date_suggestion.json", "r") as f:
                data["date_suggestion"] = json.load(f)
        except:
            data["date_suggestion"] = None
            
        return data
    
    def create_system_prompt(self, health_data):
        """Create system prompt with health context"""
        
        prompt = """You are Pyrus, an AI health coach for a magic mirror system. You have access to comprehensive health data from dual wearables:

**Your User (Whoop):**
- Recovery, Sleep, Strain, HRV, Resting HR
- 7-day trends and averages

**Wife (Oura Ring):**
- Readiness, Sleep, Activity, Steps, Resting HR  
- 7-day trends and averages

**Your Personality:**
- Warm, encouraging, and insightful
- Focus on actionable advice
- Balance health optimization with life enjoyment
- Relationship-aware (Friday date nights are tradition)

**Current Data:**
"""
        
        if health_data.get("current"):
            current = health_data["current"]
            prompt += f"\n**Today's Metrics:**\n"
            if current.get("you"):
                you = current["you"]
                prompt += f"- You: Recovery {you.get('recovery_score')}%, Sleep {you.get('sleep_hours')}h, Strain {you.get('strain')}\n"
            if current.get("wife"):
                wife = current["wife"]
                prompt += f"- Wife: Readiness {wife.get('readiness_score')}%, Sleep {wife.get('sleep_hours')}h, Steps {wife.get('steps')}\n"
        
        if health_data.get("weekly"):
            weekly = health_data["weekly"]
            prompt += f"\n**Weekly Trends:**\n"
            prompt += f"- Combined Energy: {weekly.get('combined_energy_score')}% ({weekly.get('energy_level')})\n"
            prompt += f"- Your Recovery: {weekly['whoop_weekly'].get('avg_recovery')}% ({weekly['whoop_weekly'].get('trend')})\n"
            prompt += f"- Wife's Readiness: {weekly['oura_weekly'].get('avg_readiness')}% ({weekly['oura_weekly'].get('trend')})\n"
            prompt += f"- Recommendation: {weekly.get('recommendation')}\n"
        
        if health_data.get("date_suggestion"):
            date = health_data["date_suggestion"]
            prompt += f"\n**Date Night Info:**\n"
            prompt += f"- Days since last date: {date['last_date'].get('days_since')}\n"
            prompt += f"- This week's energy: {date['weekly_health'].get('energy_score')}%\n"
            if date.get('suggested_dates'):
                top_suggestion = date['suggested_dates'][0]
                prompt += f"- Top Friday suggestion: {top_suggestion.get('title')}\n"
        
        prompt += "\nProvide personalized, actionable health coaching based on this data."
        
        return prompt
    
    def get_daily_summary(self):
        """Generate daily health summary"""
        health_data = self.load_health_data()
        system_prompt = self.create_system_prompt(health_data)
        
        user_prompt = """Give me a warm, encouraging daily health summary. Include:
1. How both of us are doing today
2. Any concerning trends to watch
3. One specific actionable recommendation for today
4. A brief note about this Friday's date night

Keep it concise (3-4 sentences) and motivating."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        return response.choices[0].message.content
    
    def ask_question(self, question):
        """Ask Pyrus a health-related question"""
        health_data = self.load_health_data()
        system_prompt = self.create_system_prompt(health_data)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description="Pyrus AI Health Coach")
    parser.add_argument("--query", type=str, help="Ask Pyrus a question")
    parser.add_argument("--daily-summary", action="store_true", help="Get daily health summary")
    
    args = parser.parse_args()
    
    coach = PyrusAICoach()
    
    if args.daily_summary:
        print("\n" + "="*60)
        print("💚 PYRUS DAILY HEALTH SUMMARY")
        print("="*60)
        summary = coach.get_daily_summary()
        print(f"\n{summary}\n")
        print("="*60 + "\n")
    elif args.query:
        print("\n" + "="*60)
        print(f"❓ YOUR QUESTION: {args.query}")
        print("="*60)
        answer = coach.ask_question(args.query)
        print(f"\n💡 PYRUS: {answer}\n")
        print("="*60 + "\n")
    else:
        print("Usage:")
        print("  python pyrus_ai_coach.py --daily-summary")
        print("  python pyrus_ai_coach.py --query 'How should I train today?'")
        sys.exit(1)


if __name__ == "__main__":
    main()
