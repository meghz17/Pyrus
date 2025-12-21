import requests
import webbrowser
import urllib.parse
import json
import os
import time
import secrets
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from supabase_client import get_token, save_token

class WhoopClient:
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: str = "https://localhost/callback",
        token_file: Optional[str] = None,
        non_interactive: bool = False
    ):
        # 1. Load Environment
        load_dotenv() # Load .env from local file if present
        
        # 2. Config
        self.client_id = client_id or os.getenv("WHOOP_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("WHOOP_CLIENT_SECRET")
        self.redirect_uri = redirect_uri
        self.non_interactive = non_interactive
        
        # 3. Validation
        if not self.client_id or not self.client_secret:
            raise ValueError("Missing WHOOP_CLIENT_ID or WHOOP_CLIENT_SECRET. Check your .env file or GitHub Secrets.")

        # 4. Paths
        if token_file:
            self.token_file = token_file
        else:
            repo_root = Path(__file__).resolve().parent.parent
            self.token_file = str(repo_root / "data" / "whoop_tokens.json")

        # 5. API Constants
        self.oauth_base_url = "https://api.prod.whoop.com"
        self.api_base_url = "https://api.prod.whoop.com/developer"
        self.scopes = "offline read:recovery read:sleep read:workout read:cycles read:profile read:body_measurement"

    def _get_token_from_env(self) -> Optional[Dict[str, Any]]:
        """Priority 1: Check for direct JSON injection in environment."""
        env_json = os.getenv("WHOOP_TOKEN_JSON")
        if env_json:
            try:
                print("DEBUG: Loaded token from WHOOP_TOKEN_JSON env var")
                return json.loads(env_json)
            except json.JSONDecodeError:
                print("⚠ Error: WHOOP_TOKEN_JSON is set but invalid JSON.")
        return None

    def _get_token_from_file(self) -> Optional[Dict[str, Any]]:
        """Priority 2: Check local filesystem."""
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, "r") as f:
                    # check if file is empty
                    content = f.read()
                    if not content:
                        return None
                    return json.loads(content)
            except Exception as e:
                print(f"DEBUG: Failed to load local token file: {e}")
        return None

    def _get_token_from_supabase(self) -> Optional[Dict[str, Any]]:
        """Priority 3: Check Supabase cloud store."""
        try:
            return get_token("whoop")
        except Exception as e:
            print(f"DEBUG: Failed to fetch token from Supabase: {e}")
            return None

    def _save_tokens(self, tokens: Dict[str, Any]) -> None:
        """
        Persist tokens to ALL available storage mechanisms.
        Failure in one shouldn't crash the program.
        """
        # 1. Local File
        try:
            os.makedirs(os.path.dirname(self.token_file) or '.', exist_ok=True)
            with open(self.token_file, 'w') as f:
                json.dump(tokens, f, indent=2)
        except Exception as e:
            # Only complain if we expected it to work (not running in a read-only environment)
            pass

        # 2. Supabase
        try:
            save_token("whoop", tokens)
            print("✓ Synced refreshed token to Supabase")
        except Exception as e:
            print(f"⚠ Warning: Failed to sync token to Supabase: {e}")

    def _refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        url = f"{self.oauth_base_url}/oauth/oauth2/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.scopes # Sometimes required by strict Oauth impls
        }
        
        response = requests.post(url, data=data)
        response.raise_for_status()
        
        new_tokens = response.json()
        new_tokens["timestamp"] = time.time()
        # Ensure refresh token is persisted if returned, else keep old one
        if "refresh_token" not in new_tokens:
            new_tokens["refresh_token"] = refresh_token
            
        return new_tokens

    def get_valid_token(self) -> str:
        """
        High-level method to return a valid access token.
        Orchestrates loading -> checking expiry -> refreshing -> saving.
        """
        # 1. Load best available token
        tokens = self._get_token_from_env() or self._get_token_from_file() or self._get_token_from_supabase()

        if not tokens:
            if self.non_interactive:
                raise Exception("CRITICAL: No Whoop tokens found in Env, File, or Supabase. Cannot run headless.")
            else:
                print("No tokens found. Starting interactive authorization...")
                return self.interactive_authorize()

        # 2. Check Expiry (Assume 1 hour life if not specified - 3600s)
        # Refresh 5 minutes (300s) before actual expiry to be safe
        now = time.time()
        created_at = tokens.get("timestamp", now)
        expires_in = tokens.get("expires_in", 3600)
        expires_at = created_at + expires_in
        
        if now >= (expires_at - 300):
            print("Token expiring soon or expired. Refreshing...")
            try:
                new_tokens = self._refresh_token(tokens["refresh_token"])
                self._save_tokens(new_tokens)
                return new_tokens["access_token"]
            except Exception as e:
                print(f"❌ Failed to refresh token: {e}")
                if self.non_interactive:
                    raise Exception("Token refresh failed in headless mode. Please re-authenticate locally.")
                return self.interactive_authorize()
        
        return tokens["access_token"]

    def interactive_authorize(self) -> str:
        """Interactive Oauth Flow for local setup."""
        state = secrets.token_urlsafe(32)
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scopes,
            "state": state
        }
        auth_url = f"{self.oauth_base_url}/oauth/oauth2/auth?{urllib.parse.urlencode(params)}"
        
        print("\n" + "="*60)
        print("WHOOP AUTHORIZATION REQUIRED")
        print("="*60)
        print(f"URL: {auth_url}\n")
        
        try:
            webbrowser.open(auth_url)
        except:
            pass
            
        print(f"1. Log in and authorize.")
        print(f"2. You will be redirected to {self.redirect_uri}")
        print("3. Copy the 'code' parameter from the URL bar.")
        
        code = input("Enter authorization code: ").strip()
        
        # Exchange Code
        token_url = f"{self.oauth_base_url}/oauth/oauth2/token"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri
        }
        
        r = requests.post(token_url, data=data)
        r.raise_for_status()
        
        tokens = r.json()
        tokens["timestamp"] = time.time()
        
        self._save_tokens(tokens)
        print("\n✅ Validated and Saved!")
        
        return tokens["access_token"]

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Authenticated request wrapper with 401 retry logic."""
        access_token = self.get_valid_token()
        url = f"{self.api_base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            r = requests.get(url, headers=headers, params=params)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print("Got 401. Assuming token expired/revoked. Retrying once...")
                # Force refresh logic by clearing 'timestamp' or just re-running get_valid_token?
                # Actually get_valid_token logic relies on time.
                # If 401 happens *within* valid time window, the token is revoked, not expired.
                # We should try to refresh it explicitly.
                
                # Check if we can refresh
                tokens = self._get_token_from_file() or self._get_token_from_supabase()
                if tokens and "refresh_token" in tokens:
                    try:
                        print("Attempting reactive refresh...")
                        new_tokens = self._refresh_token(tokens["refresh_token"])
                        self._save_tokens(new_tokens)
                        # Retry Request
                        headers["Authorization"] = f"Bearer {new_tokens['access_token']}"
                        r2 = requests.get(url, headers=headers, params=params)
                        r2.raise_for_status()
                        return r2.json()
                    except Exception as refresh_err:
                        raise Exception(f"Session expired and refresh failed: {refresh_err}")
            raise e

    # --- Public Data Methods (Pass-throughs) ---
    def get_profile(self) -> Dict[str, Any]:
        return self._make_request("v1/user/profile/basic")
    
    def get_body_measurements(self) -> Dict[str, Any]:
        return self._make_request("v2/user/measurement/body")
    
    def get_recovery(self, limit: int = 10, start: str = None, end: str = None) -> Dict[str, Any]:
        params = {"limit": limit}
        if start: params["start"] = start
        if end: params["end"] = end
        return self._make_request("v2/recovery", params)
    
    def get_sleep(self, limit: int = 10, start: str = None, end: str = None) -> Dict[str, Any]:
        params = {"limit": limit}
        if start: params["start"] = start
        if end: params["end"] = end
        return self._make_request("v2/activity/sleep", params)
    
    def get_workouts(self, limit: int = 10, start: str = None, end: str = None) -> Dict[str, Any]:
        params = {"limit": limit}
        if start: params["start"] = start
        if end: params["end"] = end
        return self._make_request("v2/activity/workout", params)
    
    def get_cycles(self, limit: int = 10, start: str = None, end: str = None) -> Dict[str, Any]:
        params = {"limit": limit}
        if start: params["start"] = start
        if end: params["end"] = end
        return self._make_request("v2/cycle", params)
