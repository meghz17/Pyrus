# JARVIS-Style Magic Mirror Health System

## Overview

This project develops a privacy-first Magic Mirror system for Raspberry Pi that integrates health data from WHOOP (user) and Oura Ring (partner) with AI-powered health coaching and relationship management. Its core purpose is to provide personalized daily guidance, emphasizing local data processing and user privacy. The system will feature AI coaching, smart date night suggestions based on health metrics, and voice interaction capabilities, aiming to create a comprehensive, intelligent personal assistant.

## User Preferences

- **Date Night Tradition**: Friday date nights (weekly)
- **Date Suggestions**: Should analyze full week's health data and suggest on Thursday only
- **Privacy**: All data stored locally, no cloud dependencies
- **AI Assistant Name**: Pyrus (smart mirror AI)

## System Architecture

### UI/UX Decisions

The Magic Mirror interface will feature custom modules:
-   **MMM-HealthDashboard**: Displays Whoop and Oura data side-by-side with color-coded metrics (Whoop red, Oura blue) and real-time updates.
-   **MMM-DateNightTracker**: Shows smart Friday date suggestions with energy-aware recommendations and urgency indicators.
-   **Pyrus AI Health Coach**: Provides daily personalized summaries and a question-and-answer interface.

### Technical Implementations & System Design

**Dual Wearable Health Data Integration:**
-   **WHOOP (User)**: Fetches recovery, sleep, strain, workouts, cycles, and body measurements via OAuth 2.0.
-   **Oura Ring (Partner)**: Fetches sleep, readiness, activity, SpO2, heart rate, stress, and workouts via Personal Access Token.
-   Data is fetched daily, combined, and then analyzed weekly to calculate 7-day averages and trends.
-   All collected health data is made available to the Pyrus AI for comprehensive context.

**Date Night Management System:**
-   **Database**: SQLite is used for storing date history, including location, type, description, rating, cost, and notes, with full CRUD operations.
-   **Smart Suggestion Engine**: Contains 113 curated date ideas categorized by type, budget, energy level, season, and indoor/outdoor preference.
-   **Health-Aware Recommendations**: Utilizes the combined weekly energy levels from both partners to suggest appropriate dates (e.g., high-energy dates for high combined energy).
-   **Thursday-Friday Logic**: The system suggests dates for the upcoming Friday, running only on Thursdays, and respects a 14-day threshold for the last date.

**AI Integration (Pyrus):**
-   Pyrus AI, powered by GPT-4, provides health coaching, daily summaries, and relationship-aware recommendations.
-   It has access to real-time and historical health data, date night history, and contextual awareness (day of week, season, combined energy levels).

**Security & Privacy:**
-   All API credentials are stored in Replit Secrets.
-   OAuth tokens are stored ephemerally in `/tmp/` and are not committed to version control.
-   All data processing is designed to occur locally to ensure privacy.

**Deployment & Automation:**
-   Designed for Raspberry Pi, with an `install.sh` script for automated setup of MagicMirror², custom modules, Python health monitoring, cron jobs, and PM2.
-   Automated cron jobs are scheduled for daily health data fetching/combining and weekly health analysis/date suggestions.

## External Dependencies

-   **WHOOP API**: For retrieving user's health and activity data (requires OAuth 2.0).
-   **Oura API**: For retrieving partner's health and activity data (currently uses Personal Access Token).
-   **OpenAI API**: Integrated for the Pyrus AI Health Coach (GPT-4 powered coaching).
-   **`requests`**: Python library for making HTTP requests to external APIs.
-   **`python-dotenv`**: Python library for managing environment variables.

---

## Phase 3 Roadmap - Life Management Integration
**Date: October 20, 2025**

### 🎯 Vision
Expand Pyrus from a health & relationship assistant into a complete life management system with vehicle tracking, financial insights, gamified fitness, and deep AI personalization through historical data learning.

### 🚗 Feature 1: Tesla Integration
**Objective:** Real-time vehicle charging and status monitoring on the Magic Mirror.

**Implementation:**
- Create `tesla_client.py` for Tesla API integration
- Fetch: Battery level, charging status, range, location, estimated charge completion
- Store charging history in PostgreSQL for pattern analysis
- Display on new `MMM-TeslaStatus` MagicMirror module
- AI insights: "Your Tesla is at 45% - start charging for tomorrow's drive"

**Data Points:**
- Battery percentage & range
- Charging state (idle/charging/complete)
- Location (home/away)
- Charge rate & time to full
- Historical charging patterns

### 💰 Feature 2: Monarch Money Net Worth Tracking
**Objective:** Integrate financial health into the overall life dashboard.

**Implementation:**
- Create `monarch_client.py` for Monarch Money API
- Fetch: Total net worth, account balances, monthly trends, budget vs. spending
- Store financial snapshots in PostgreSQL (daily or weekly)
- Display on new `MMM-NetWorth` MagicMirror module
- AI insights: "Net worth up 3% this month - you're crushing your fitness AND financial goals!"

**Data Points:**
- Total net worth
- Account breakdown (checking, savings, investments)
- Monthly change percentage
- Budget performance
- Spending categories

### 🎮 Feature 3: Gamified Fitness Goals
**Objective:** Weekly personalized fitness challenges with AI-powered goal setting based on historical performance.

**Implementation:**
- Create `fitness_gamification.py` system
- Analyze monthly historical data to set realistic weekly goals
- Generate personalized challenges: "Beat last week's strain by 10%"
- Track achievements, streaks, and milestones
- Display on new `MMM-FitnessGoals` MagicMirror module with progress bars
- AI learning: "You always perform best after 8+ hours of sleep - prioritize rest this week"

**Gamification Elements:**
- Weekly goals (strain, recovery, sleep, steps)
- Achievement badges (7-day streak, personal records)
- Progress bars and visual feedback
- Personalized recommendations based on patterns
- Monthly performance reviews

**AI Personalization:**
- Analyze: Sleep → Performance correlations
- Identify: Best recovery days for high-strain activities
- Suggest: Optimal training timing based on your patterns
- Learn: What motivates you (streaks, challenges, achievements)

### 💾 Feature 4: Database Architecture Upgrade
**Objective:** Transition from ephemeral JSON files to persistent PostgreSQL database for deep historical analysis and AI learning.

**Current State:**
- Health data stored in JSON files (overwritten daily)
- No historical tracking beyond 7 days
- Limited AI personalization without long-term data

**New Architecture:**

**PostgreSQL Tables:**
```
daily_health:
- date, whoop_data (JSON), oura_data (JSON)
- recovery_score, readiness_score, sleep_hours, strain, hrv, resting_hr, steps

weekly_summaries:
- week_start_date, avg_recovery, avg_readiness, combined_energy
- trend, recommendation, goals_met

monthly_patterns:
- month, best_sleep_duration, optimal_recovery_days, strain_capacity
- performance_insights (JSON), learned_patterns (JSON)

tesla_status:
- timestamp, battery_level, charging_state, range, location

net_worth:
- date, total_net_worth, monthly_change, accounts (JSON)

fitness_goals:
- week_start_date, goals (JSON), achievements (JSON), streak_count
```

**Data Flow:**
```
Daily (6 AM):
  API → PostgreSQL (INSERT daily snapshot)
  API → JSON file (for today's mirror display)

Weekly (Thursday):
  PostgreSQL → Analyze 7 days → Generate goals/suggestions
  Results → JSON + Database

Monthly (1st):
  PostgreSQL → Analyze 30 days → Learn patterns
  Update AI personalization model
```

**Benefits:**
- Historical trend analysis (year-over-year comparisons)
- AI learns YOUR patterns (not generic advice)
- Export data for external analysis
- Never lose historical health data
- Deeper insights: "Your recovery is 15% better than this time last year"

### 📅 Implementation Plan

**Phase 3.1: Database Foundation**
1. Create PostgreSQL schema with all tables
2. Migrate existing health fetchers to dual-write (JSON + Database)
3. Create data migration scripts for historical data
4. Update weekly/monthly analyzers to read from database

**Phase 3.2: API Integrations**
5. Tesla API client + database integration
6. Monarch Money API client + database integration
7. Automated data fetching (cron jobs)
8. Error handling and token management

**Phase 3.3: Gamification & AI Learning**
9. Fitness goal generator with historical analysis
10. Monthly pattern learning engine
11. Achievement tracking system
12. Personalized recommendation engine

**Phase 3.4: MagicMirror Modules**
13. MMM-TeslaStatus (vehicle info display)
14. MMM-NetWorth (financial dashboard)
15. MMM-FitnessGoals (weekly goals + progress)
16. Update existing modules to use database

**Phase 3.5: AI Enhancement**
17. Update Pyrus AI to access full historical database
18. Add Tesla/financial awareness to coaching
19. Implement pattern-based recommendations
20. Create monthly performance reviews

**Phase 3.6: Deployment & Testing**
21. Update Raspberry Pi installer for PostgreSQL
22. Add new cron jobs (monthly analysis)
23. Update documentation and configuration examples
24. End-to-end testing of all features

### 🔐 API Requirements

**New Secrets Needed:**
- `TESLA_ACCESS_TOKEN` (or OAuth flow)
- `TESLA_REFRESH_TOKEN`
- `MONARCH_EMAIL`
- `MONARCH_PASSWORD` (or API token if available)
- `DATABASE_URL` (PostgreSQL connection string)

### 📊 Expected Outcomes

**Quantitative:**
- 12+ months of historical health data stored
- 3 new data sources (Tesla, Monarch, Fitness Goals)
- 5+ new database tables
- 3 new MagicMirror modules
- Monthly AI learning cycles

**Qualitative:**
- Truly personalized health coaching (based on YOUR patterns)
- Complete life dashboard (health, vehicle, finances)
- Gamified motivation system
- Deeper insights from long-term trend analysis
- Single source of truth for all personal data

### 🎨 User Experience Enhancements

**Morning Mirror View:**
- "Good morning! Tesla: 85% charged, ready for work"
- "Net worth up 2% this month - great progress!"
- "You're 60% toward your weekly strain goal - keep crushing it!"
- Pyrus AI: "Based on your sleep patterns, today is perfect for a high-intensity workout"

**Thursday Evening:**
- Weekly fitness review: "5-day workout streak! 🔥"
- Financial insight: "Spending on track, budget 95% achieved"
- Date night suggestion: "High energy week - try that new rock climbing gym!"

**Monthly Review:**
- "Best month yet! Recovery improved 12% from last month"
- "You perform 23% better after 8+ hours of sleep"
- "Tesla charging cost down 15% with off-peak scheduling"

---

## Recent Updates

### October 20, 2025 - WHOOP Token Persistence Fix
**Problem:** WHOOP authentication tokens were stored in `/tmp/`, causing them to be wiped on Replit restarts. Users had to manually re-authenticate every time.

**Solution Implemented:**
- Moved token storage to persistent `data/whoop_tokens.json` with absolute path resolution
- Added `WHOOP_TOKEN_FILE` environment variable override for custom paths
- Implemented atomic file writes (tempfile + os.replace) to prevent corruption
- Added automatic directory creation for fresh deployments
- Smart 401 handling: attempts token refresh before re-authentication
- Selective token deletion: only removes on explicit `invalid_grant`, preserves on transient errors
- **Non-interactive mode**: Cron jobs fail fast with helpful error messages instead of hanging on input prompts
- Works from any working directory (critical for cron jobs on Raspberry Pi)

**Result:** Production-ready for Raspberry Pi cron automation. Tokens persist across restarts, auto-refresh before expiry, and automated jobs never hang.

---

## Current Project Status

**Phase 1 (Complete):** ✅
- Dual wearable integration
- Date night tracking system
- 113 curated date ideas
- Weekly health analysis

**Phase 2 (Complete):** ✅
- 3 custom MagicMirror modules
- Pyrus AI Health Coach (GPT-4)
- Raspberry Pi deployment package
- Complete documentation
- Production-ready WHOOP token persistence

**Phase 3 (Planned):** 📋
- Tesla integration
- Monarch Money tracking
- Gamified fitness goals
- PostgreSQL database migration
- AI learning engine