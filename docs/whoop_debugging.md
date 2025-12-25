# Whoop API Debugging Guide

## The Problem
Your V1 Python code was working with `v2/recovery` endpoint, but n8n is getting 404 errors with the same endpoint.

## Root Cause
The 404 is likely because:
1. **Missing Redirect URI** in Whoop developer portal for n8n's OAuth callback
2. **Incomplete OAuth flow** - the access token might not have the right scopes

---

## Solution 1: Fix the Redirect URI (Recommended)

### Step 1: Add n8n's Redirect URI to Whoop App
1. Go to [developer.whoop.com](https://developer.whoop.com)
2. Click on your app ("Meghz")
3. Find **"Redirect URIs"** section
4. Add this EXACT URL:
   ```
   http://localhost:5678/rest/oauth2-credential/callback
   ```
5. Click **Save**

### Step 2: Delete and Recreate OAuth Credential in n8n
1. In n8n, go to **Credentials** (left sidebar)
2. Find your Whoop OAuth2 credential
3. Delete it
4. Go back to "Get Whoop (Partner A)" node
5. Create a NEW OAuth2 credential with:
   - Authorization URL: `https://api.prod.whoop.com/oauth/oauth2/auth`
   - Access Token URL: `https://api.prod.whoop.com/oauth/oauth2/token`
   - Client ID: `da93b1ae-2121-47ce-b64b-b4b405aedd79`
   - Client Secret: `965da6aafc105cfd57b371babee832a25c8891f329da69a8f9406c173f6d5bff`
   - Scope: `read:recovery read:cycles read:sleep`
   - Authentication: `Body`

### Step 3: Connect Account
1. Click **"Connect my account"**
2. Sign in to Whoop
3. Authorize the app
4. You should be redirected back to n8n

### Step 4: Test
Click **"Execute Node"** on the Whoop node.

---

## Solution 2: Use Your Working Python Code (Alternative)

If OAuth continues to fail, we can bypass n8n for Whoop and use your existing Python client:

### Create a Simple Wrapper Script

Create `/Users/meghr/Desktop/Pyrus-main/scripts/fetch_whoop_for_n8n.py`:

```python
#!/usr/bin/env python3
import sys
sys.path.append('/Users/meghr/Desktop/Pyrus-main/src')

from whoop_client import WhoopClient
from datetime import datetime, timedelta
import json

# Initialize client (will use your existing tokens)
client = WhoopClient(non_interactive=True)

# Get yesterday's recovery
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
today = datetime.now().strftime('%Y-%m-%d')

recovery_data = client.get_recovery(limit=1, start=yesterday, end=today)

# Output JSON for n8n to consume
print(json.dumps(recovery_data))
```

### Update n8n Node

Change "Get Whoop (Partner A)" to use **Execute Command** node instead:

**Command:**
```bash
python3 /Users/meghr/Desktop/Pyrus-main/scripts/fetch_whoop_for_n8n.py
```

This leverages your already-working OAuth setup!

---

## Solution 3: Check Whoop App Status

Your app might need approval for production API access:

1. Go to [developer.whoop.com](https://developer.whoop.com)
2. Check if your app status shows "Development" or "In Review"
3. If it says "9 remaining test users", you're in sandbox mode
4. The v2 API might require production approval

**To request production access:**
- Email: developer@whoop.com
- Subject: "Production API Access Request for [Your App Name]"
- Include your Client ID

---

## Quick Test: Verify Endpoint Works

Run this curl command to test if the endpoint is accessible:

```bash
# Replace YOUR_ACCESS_TOKEN with a valid token
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://api.prod.whoop.com/developer/v2/recovery?limit=1"
```

If this returns data, the endpoint works and it's an n8n OAuth issue.
If this returns 404, your app needs production approval.

---

## Recommended Approach

1. **Try Solution 1 first** (fix redirect URI)
2. If that fails, **use Solution 2** (Python wrapper) - this is guaranteed to work since your V1 code is already functional
3. If you want full n8n integration, **pursue Solution 3** (production approval)

For now, Solution 2 is the fastest path to a working system!
