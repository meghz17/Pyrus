#!/bin/bash
# setup_env.sh - Setup environment variables for Pyrus Life OS

DOTENV_FILE=".env"

echo "=========================================================="
echo "          Pyrus Life OS - Environment Setup               "
echo "=========================================================="

if [ -f "$DOTENV_FILE" ]; then
    echo "⚠️  $DOTENV_FILE already exists."
    read -p "Do you want to overwrite it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup aborted."
        exit 1
    fi
fi

echo "Please enter your credentials (press Enter to skip):"

read -p "Oura Access Token: " OURA_ACCESS_TOKEN
read -p "Whoop Client ID: " WHOOP_CLIENT_ID
read -p "Whoop Client Secret: " WHOOP_CLIENT_SECRET
read -p "OpenAI API Key: " OPENAI_API_KEY
read -p "OpenAI Base URL (default: http://localhost:1106/modelfarm/openai): " OPENAI_BASE_URL
OPENAI_BASE_URL=${OPENAI_BASE_URL:-"http://localhost:1106/modelfarm/openai"}

# Generate session secret if not exists
SESSION_SECRET=$(openssl rand -base64 64)

cat <<EOF > "$DOTENV_FILE"
# Oura Ring API
OURA_ACCESS_TOKEN=$OURA_ACCESS_TOKEN

# Whoop Developer API
WHOOP_CLIENT_ID=$WHOOP_CLIENT_ID
WHOOP_CLIENT_SECRET=$WHOOP_CLIENT_SECRET

# OpenAI Integration
AI_INTEGRATIONS_OPENAI_API_KEY=$OPENAI_API_KEY
AI_INTEGRATIONS_OPENAI_BASE_URL=$OPENAI_BASE_URL

# Web Dashboard Session
SESSION_SECRET=$SESSION_SECRET
EOF

chmod 600 "$DOTENV_FILE"

echo "✅ $DOTENV_FILE has been created successfully."
echo "🔒 File permissions set to private (600)."
echo "=========================================================="
