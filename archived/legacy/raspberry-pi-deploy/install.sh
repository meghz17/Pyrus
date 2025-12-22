#!/bin/bash
# Pyrus Magic Mirror Installation Script for Raspberry Pi
# This script installs MagicMirror² and all Pyrus custom modules

set -e

# Store deployment directory at the very beginning
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEPLOY_DIR="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo "🪞 PYRUS MAGIC MIRROR INSTALLATION"
echo "============================================================"
echo ""
echo "Deployment directory: $DEPLOY_DIR"
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ] || ! grep -q "Raspberry Pi" /proc/device-tree/model; then
    echo "⚠️  Warning: This doesn't appear to be a Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system
echo "📦 Updating system packages..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Node.js 22+
echo ""
echo "📦 Installing Node.js 22..."
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 22 ]; then
    echo "❌ Error: Node.js 22+ required. Found: $(node --version)"
    exit 1
fi

echo "✅ Node.js $(node --version) installed"

# Install Python 3.11+
echo ""
echo "📦 Installing Python 3.11..."
sudo apt-get install -y python3 python3-pip python3-venv

# Install Git
echo ""
echo "📦 Installing Git..."
sudo apt-get install -y git

# Clone MagicMirror²
echo ""
echo "📦 Installing MagicMirror²..."
cd ~
if [ -d "MagicMirror" ]; then
    echo "⚠️  MagicMirror directory already exists. Skipping clone."
else
    git clone https://github.com/MagicMirrorOrg/MagicMirror
fi

cd ~/MagicMirror

# Install MagicMirror dependencies
echo "📦 Installing MagicMirror dependencies (this may take 10-15 minutes)..."
npm run install-mm

# Create config if doesn't exist
if [ ! -f config/config.js ]; then
    echo "📝 Creating default config..."
    cp config/config.js.sample config/config.js
fi

# Install custom Pyrus modules
echo ""
echo "📦 Installing Pyrus custom modules..."

# MMM-HealthDashboard
if [ ! -d ~/MagicMirror/modules/MMM-HealthDashboard ]; then
    cp -r "$DEPLOY_DIR/magicmirror-modules/MMM-HealthDashboard" ~/MagicMirror/modules/
    if [ $? -eq 0 ]; then
        echo "✅ MMM-HealthDashboard installed"
    else
        echo "❌ Error installing MMM-HealthDashboard"
        exit 1
    fi
fi

# MMM-DateNightTracker
if [ ! -d ~/MagicMirror/modules/MMM-DateNightTracker ]; then
    cp -r "$DEPLOY_DIR/magicmirror-modules/MMM-DateNightTracker" ~/MagicMirror/modules/
    if [ $? -eq 0 ]; then
        echo "✅ MMM-DateNightTracker installed"
    else
        echo "❌ Error installing MMM-DateNightTracker"
        exit 1
    fi
fi

# Install Python health data scripts
echo ""
echo "📦 Installing Python health monitoring scripts..."
mkdir -p ~/pyrus-health
cp -r "$DEPLOY_DIR/src"/* ~/pyrus-health/
if [ -d "$DEPLOY_DIR/data" ]; then
    cp -r "$DEPLOY_DIR/data" ~/pyrus-health/
fi

# Create data output directory
mkdir -p ~/pyrus-health/data

# Create directory symlink so MagicMirror can read Python output
# Remove existing data directory/link if present
rm -rf ~/MagicMirror/data
# Create symlink to Python data directory
ln -sfn ~/pyrus-health/data ~/MagicMirror/data
echo "✅ Data directory linked to ~/pyrus-health/data"

# Install Python dependencies
cd ~/pyrus-health
pip3 install --user requests python-dotenv openai

# Setup cron jobs
echo ""
echo "📅 Setting up cron jobs..."
(crontab -l 2>/dev/null; echo "# Pyrus Health Data Fetchers") | crontab -
(crontab -l 2>/dev/null; echo "0 6 * * * cd ~/pyrus-health && python3 fetch_daily_whoop.py") | crontab -
(crontab -l 2>/dev/null; echo "5 6 * * * cd ~/pyrus-health && python3 fetch_daily_oura.py") | crontab -
(crontab -l 2>/dev/null; echo "10 6 * * * cd ~/pyrus-health && python3 health_combiner.py") | crontab -
(crontab -l 2>/dev/null; echo "0 17 * * 4 cd ~/pyrus-health && python3 weekly_health_analyzer.py") | crontab -
(crontab -l 2>/dev/null; echo "0 18 * * 4 cd ~/pyrus-health && python3 friday_date_suggester.py") | crontab -
echo "✅ Cron jobs configured"

# Setup PM2 for auto-start
echo ""
echo "📦 Installing PM2 for auto-start..."
sudo npm install -g pm2

# Start MagicMirror with PM2
cd ~/MagicMirror
pm2 start npm --name MagicMirror -- start
pm2 save
pm2 startup | tail -1 | bash

echo ""
echo "============================================================"
echo "✅ INSTALLATION COMPLETE!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Configure API credentials:"
echo "   nano ~/pyrus-health/.env"
echo "   (Add WHOOP_CLIENT_ID, WHOOP_CLIENT_SECRET, OURA_ACCESS_TOKEN)"
echo ""
echo "2. Update MagicMirror config:"
echo "   nano ~/MagicMirror/config/config.js"
echo "   (Use config-example.js as template)"
echo ""
echo "3. Restart MagicMirror:"
echo "   pm2 restart MagicMirror"
echo ""
echo "4. View logs:"
echo "   pm2 logs MagicMirror"
echo ""
echo "5. Access mirror at: http://$(hostname -I | awk '{print $1}'):8080"
echo ""
echo "============================================================"
