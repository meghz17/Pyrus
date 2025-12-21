# Whoop API Client

A Python API client for querying personal Whoop health data with OAuth 2.0 authentication and automatic token management.

## Features

- **OAuth 2.0 Authentication**: Automatic authorization flow with token persistence
- **Automatic Token Refresh**: Handles token expiration transparently
- **Complete API Coverage**: Access all Whoop v2 API endpoints
  - User profile and body measurements
  - Recovery data (HRV, resting heart rate, recovery score)
  - Sleep data (performance metrics, sleep stages)
  - Workout data (strain scores, heart rate)
  - Physiological cycles
- **Paginated Queries**: Retrieve data with customizable date ranges and limits
- **Type Hints**: Full type annotations for better IDE support

## Setup

### 1. Get Whoop API Credentials

1. Visit [https://developer.whoop.com/](https://developer.whoop.com/)
2. Create an application
3. Note your Client ID and Client Secret
4. Add redirect URI: `https://localhost/callback` to your app's allowed redirect URIs

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
WHOOP_CLIENT_ID=your_client_id_here
WHOOP_CLIENT_SECRET=your_client_secret_here
WHOOP_REDIRECT_URI=https://localhost/callback
```

**Note:** In Replit, use the Secrets tab to add `WHOOP_CLIENT_ID` and `WHOOP_CLIENT_SECRET` securely instead of creating a `.env` file.

### 3. Run the Example

First-time setup requires authorization:

```bash
python example.py
```

The authorization process:
1. Opens your browser to the Whoop authorization page
2. You approve the app and get redirected to a URL with a code
3. Copy the code from the URL and paste it when prompted
4. Your access token is saved for future use (no need to re-authorize)

### 4. Quick Summary

Get a quick summary of your latest Whoop data:

```bash
python get_whoop_summary.py
```

This displays your latest recovery, sleep, workout, and body measurements in a clean format.

## Usage

### Basic Example

```python
from whoop_client import WhoopClient
import os

client = WhoopClient(
    client_id=os.getenv("WHOOP_CLIENT_ID"),
    client_secret=os.getenv("WHOOP_CLIENT_SECRET")
)

# Get user profile
profile = client.get_profile()
print(profile)

# Get latest recovery data
recovery = client.get_recovery(limit=5)
print(recovery)

# Get sleep data for specific date range
sleep = client.get_sleep(
    limit=10,
    start="2025-01-01T00:00:00Z",
    end="2025-01-31T23:59:59Z"
)
print(sleep)
```

### Available Methods

#### User Data
- `get_profile()` - Get basic user profile (name, email)
- `get_body_measurements()` - Get height, weight, max heart rate

#### Recovery
- `get_recovery(limit, start, end, next_token)` - Get recovery data
- `get_recovery_for_cycle(cycle_id)` - Get recovery for specific cycle

#### Sleep
- `get_sleep(limit, start, end, next_token)` - Get sleep sessions
- `get_sleep_by_id(sleep_id)` - Get specific sleep session
- `get_sleep_for_cycle(cycle_id)` - Get sleep for specific cycle

#### Workouts
- `get_workouts(limit, start, end, next_token)` - Get workouts
- `get_workout_by_id(workout_id)` - Get specific workout

#### Cycles
- `get_cycles(limit, start, end, next_token)` - Get physiological cycles
- `get_cycle_by_id(cycle_id)` - Get specific cycle

#### Access Management
- `revoke_access()` - Revoke OAuth access and delete local tokens

### Pagination

For endpoints that support pagination, use the `next_token` from the response:

```python
# Get first page
page1 = client.get_recovery(limit=25)
next_token = page1.get("next_token")

# Get next page
if next_token:
    page2 = client.get_recovery(limit=25, next_token=next_token)
```

## Token Management

### Secure Token Storage

**⚠️ IMPORTANT SECURITY NOTE:**

OAuth tokens are stored in `/tmp/whoop_tokens.json` by default. This location is specifically chosen for security:

- **Ephemeral Storage**: The `/tmp` directory is cleared when the Repl restarts, preventing long-term token exposure
- **Not Visible in File Tree**: Files in `/tmp` are not visible in public Repls, protecting your active authentication tokens
- **Best Practice for Public Repls**: If your Repl is public, never store tokens in the project root directory

### Token Lifecycle

- Tokens are automatically saved to `/tmp/whoop_tokens.json` after authorization
- Access tokens are automatically refreshed when expired
- You will need to re-authenticate after each Repl restart (since `/tmp` is ephemeral)

### If Your Tokens Were Exposed

If you previously had tokens in a visible location (like `whoop_tokens.json` in the project root):

1. **Revoke Access Immediately**: Visit [Whoop Developer Portal](https://developer.whoop.com/) and revoke access for your application
2. **Regenerate Credentials**: Consider regenerating your Client ID and Client Secret
3. **Re-authorize**: Run the app again to generate new tokens in the secure `/tmp` location

### Custom Token Location

If you need a different token storage location (for private Repls or local development):

```python
client = WhoopClient(
    client_id=os.getenv("WHOOP_CLIENT_ID"),
    client_secret=os.getenv("WHOOP_CLIENT_SECRET"),
    token_file="/path/to/your/secure/location.json"
)
```

## API Reference

Full Whoop API documentation: [https://developer.whoop.com/api](https://developer.whoop.com/api)

## License

This project is provided as-is for personal use with the Whoop API.
