# Pyrus Magic Mirror - Raspberry Pi Deployment Guide

Complete deployment package for installing the Pyrus Magic Mirror system on Raspberry Pi.

## 🎯 What You'll Get

- **MagicMirror²** framework with custom modules
- **Dual Wearable Integration** (Whoop + Oura Ring)
- **AI Health Coach** powered by GPT-4
- **Smart Date Night Tracker** with Friday suggestions
- **Automated Data Fetching** via cron jobs
- **Auto-start on Boot** via PM2

---

## 📋 Prerequisites

### Hardware
- **Raspberry Pi 4 or 5** (recommended)
- **16GB+ microSD card**
- **Monitor** with HDMI input
- **Internet connection**

### Software
- **Raspberry Pi OS** (Bookworm or later)
- Fresh install recommended

### API Access
- **Whoop Developer Account** (OAuth credentials)
- **Oura Personal Access Token**
- **Replit Account** (for OpenAI integration) OR OpenAI API key

---

## 🚀 Quick Installation

### 1. Transfer Files to Raspberry Pi

```bash
# On your computer, create deployment package
scp -r raspberry-pi-deploy pi@raspberrypi.local:~/pyrus-deploy
scp -r magicmirror-modules pi@raspberrypi.local:~/pyrus-deploy/
scp -r src pi@raspberrypi.local:~/pyrus-deploy/
scp -r data pi@raspberrypi.local:~/pyrus-deploy/
scp .env.example pi@raspberrypi.local:~/pyrus-deploy/
```

### 2. Run Installation Script

```bash
# SSH into Raspberry Pi
ssh pi@raspberrypi.local

# Navigate to deployment directory
cd ~/pyrus-deploy/raspberry-pi-deploy

# Make install script executable
chmod +x install.sh

# Run installation (takes 15-20 minutes)
./install.sh
```

---

## ⚙️ Configuration

### 1. Setup API Credentials

```bash
cd ~/pyrus-health
cp .env.example .env
nano .env
```

Add your credentials:
```
WHOOP_CLIENT_ID=your_whoop_client_id
WHOOP_CLIENT_SECRET=your_whoop_client_secret
OURA_ACCESS_TOKEN=your_oura_token
AI_INTEGRATIONS_OPENAI_BASE_URL=https://api.openai.com/v1
AI_INTEGRATIONS_OPENAI_API_KEY=your_openai_key
```

### 2. Configure MagicMirror

```bash
nano ~/MagicMirror/config/config.js
```

Use the provided `config-example.js` as a template, or add custom modules to your existing config:

```javascript
{
    module: "MMM-HealthDashboard",
    position: "middle_center",
    config: {
        updateInterval: 60000,
        dataFile: "data/combined_health.json"
    }
},
{
    module: "MMM-DateNightTracker",
    position: "bottom_left",
    config: {
        dataFile: "data/friday_date_suggestion.json"
    }
}
```

### 3. Initial OAuth Authorization

```bash
# First-time Whoop authorization
cd ~/pyrus-health
python3 fetch_daily_whoop.py
# Follow the authorization URL and paste the callback
```

---

## 🔄 Starting & Managing

### Start/Stop/Restart
```bash
pm2 restart MagicMirror
pm2 stop MagicMirror
pm2 start MagicMirror
```

### View Logs
```bash
pm2 logs MagicMirror
```

### Manual Data Fetch
```bash
cd ~/pyrus-health
python3 fetch_daily_whoop.py
python3 fetch_daily_oura.py
python3 health_combiner.py
```

### Test AI Coach
```bash
cd ~/pyrus-health
python3 pyrus_ai_coach.py --daily-summary
python3 pyrus_ai_coach.py --query "How should I train today?"
```

---

## 📅 Automated Schedule (Cron Jobs)

| Time | Task | Script |
|------|------|--------|
| Daily 6:00 AM | Fetch Whoop data | `fetch_daily_whoop.py` |
| Daily 6:05 AM | Fetch Oura data | `fetch_daily_oura.py` |
| Daily 6:10 AM | Combine health data | `health_combiner.py` |
| Thu 5:00 PM | Weekly health analysis | `weekly_health_analyzer.py` |
| Thu 6:00 PM | Friday date suggestions | `friday_date_suggester.py` |

View cron jobs:
```bash
crontab -l
```

---

## 🎨 Customization

### Change Colors
Edit `~/MagicMirror/config/config.js`:
```javascript
{
    module: "MMM-HealthDashboard",
    config: {
        whoopColor: "#YOUR_COLOR",
        ouraColor: "#YOUR_COLOR"
    }
}
```

### Add More Modules
Browse: https://modules.magicmirror.builders/

### Modify Display
Edit CSS files in:
- `~/MagicMirror/modules/MMM-HealthDashboard/MMM-HealthDashboard.css`
- `~/MagicMirror/modules/MMM-DateNightTracker/MMM-DateNightTracker.css`

---

## 🐛 Troubleshooting

### MagicMirror won't start
```bash
pm2 logs MagicMirror
# Check for errors
```

### No health data showing
```bash
cd ~/pyrus-health
ls -la data/
# Verify JSON files exist and have recent timestamps

# Test data fetching
python3 fetch_daily_whoop.py
python3 fetch_daily_oura.py
```

### Black screen
```bash
# Check Node.js version (need 22+)
node --version

# Restart MagicMirror
pm2 restart MagicMirror
```

### Cron jobs not running
```bash
# Check cron log
grep CRON /var/log/syslog | tail -20

# Test script manually
cd ~/pyrus-health
python3 fetch_daily_whoop.py
```

---

## 📊 Data Files Location

All health data stored in: `~/pyrus-health/data/`

- `whoop_daily.json` - Your daily Whoop metrics
- `oura_daily.json` - Wife's daily Oura metrics
- `combined_health.json` - Unified health data
- `weekly_health_analysis.json` - 7-day trends
- `friday_date_suggestion.json` - Date recommendations

---

## 🔒 Security

- All credentials in `~/.env` (not committed to git)
- OAuth tokens in `/tmp/whoop_tokens.json` (ephemeral)
- Data processing happens locally
- No cloud dependencies (except API calls)

---

## 📝 Support

- **MagicMirror Docs**: https://docs.magicmirror.builders/
- **Forum**: https://forum.magicmirror.builders/
- **Whoop API**: https://developer.whoop.com/
- **Oura API**: https://cloud.ouraring.com/docs/

---

## 📄 License

MIT - See individual module LICENSE files
