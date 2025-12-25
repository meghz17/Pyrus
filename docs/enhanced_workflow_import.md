# Enhanced Joint Battery - Import Guide

## ✅ What's Ready

**Backend:** Fully operational with comprehensive health data collection and wellness scoring

**Workflow:** Generated at `/Users/meghr/Desktop/Pyrus-main/n8n_workflows/enhanced_health_pipeline.json`

**Total Nodes:** 15 (vs 8 in the old workflow)

---

## 📥 How to Import

### Step 1: Open n8n
Go to [http://localhost:5678](http://localhost:5678)

### Step 2: Import Workflow
1. Click **"+"** (Add Workflow)
2. Click **"Import from File"**
3. Select: `/Users/meghr/Desktop/Pyrus-main/n8n_workflows/enhanced_health_pipeline.json`
4. Click **"Import"**

### Step 3: Configure Credentials
The workflow needs 2 credentials (same as before):

**1. Whoop OAuth2**
- Node: "Whoop Recovery", "Whoop Sleep", "Whoop Cycle"
- Select your existing Whoop OAuth2 credential

**2. Oura API**
- Node: "Oura Readiness", "Oura Sleep", "Oura Activity"
- Select your existing Oura credential

### Step 4: Update Telegram Bot Token (if needed)
- Node: "Send Telegram"
- URL already has your bot token: `8318826480:AAHAJ3-QQoNIg4jFJIkNEk-TlGD5rIOwXGs`
- Chat ID already set: `6283940658`

### Step 5: Save & Activate
1. Click **"Save"** (top right)
2. Toggle **"Active"** (top right)

---

## 🧪 Testing

### Manual Test
1. Click **"Execute Workflow"** button (bottom)
2. Watch the nodes execute in sequence
3. Check Telegram for the enhanced message

### Expected Telegram Message
```
🌟 Daily Wellness Report

Partner A: 78% ✅
Partner B: 86% 🔥

💡 Today's Suggestions:
✨ Perfect day for a date night!
💪 Great day for a couples workout!

📅 Upcoming Optimal Days:
- Dec 26: Both at 85%+ (Perfect for hiking)
```

---

## 🔍 What Each Node Does

**Data Collection (7 nodes):**
1. Morning Trigger - Runs at 8 AM daily
2-4. Whoop APIs - Recovery, Sleep, Cycle
5-7. Oura APIs - Readiness, Sleep, Activity

**Data Processing (4 nodes):**
8. Merge Whoop Data - Combines 3 Whoop responses
9. Merge Oura Data - Combines 3 Oura responses
10. Save Whoop - Stores to `whoop_metrics` table
11. Save Oura - Stores to `oura_metrics` table

**Intelligence (4 nodes):**
12. Calculate Wellness - Holistic scoring algorithm
13. Generate Suggestions - Activity recommendations
14. Format Message - Creates rich Telegram text
15. Send Telegram - Delivers notification

---

## 🐛 Troubleshooting

**"Merge Whoop Data" fails:**
- Check that all 3 Whoop nodes executed successfully
- Verify Whoop OAuth credential is connected

**"Merge Oura Data" fails:**
- Check that all 3 Oura nodes executed successfully
- Verify Oura API credential is connected

**"Calculate Wellness" returns insufficient_data:**
- Data hasn't been saved to DB yet
- Wait for "Save Whoop" and "Save Oura" to complete first

**Telegram message is blank:**
- Check "Generate Suggestions" node output
- Verify the format in "Format Message" node

---

## 📊 Database Tables

Check what's being stored:

```sql
-- View Whoop data
SELECT * FROM whoop_metrics ORDER BY date DESC LIMIT 5;

-- View Oura data
SELECT * FROM oura_metrics ORDER BY date DESC LIMIT 5;

-- View wellness scores
SELECT * FROM wellness_scores ORDER BY date DESC LIMIT 5;

-- View suggestions
SELECT * FROM activity_suggestions ORDER BY date DESC LIMIT 5;
```

Run in pgAdmin: [http://localhost:5050](http://localhost:5050)

---

## 🚀 Next Steps

1. Import the workflow
2. Test manually
3. Let it run automatically at 8 AM tomorrow
4. Review the enhanced Telegram messages
5. Provide feedback for further improvements!
