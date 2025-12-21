import requests
import webbrowser
import urllib.parse
import json
import os
import time
import secrets
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime


from dotenv import load_dotenv

class WhoopClient:
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: str = "https://localhost/callback",
        token_file: Optional[str] = None,
        non_interactive: bool = False
    ):
        load_dotenv()
        self.client_id = client_id or os.getenv("WHOOP_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("WHOOP_CLIENT_SECRET")
        self.redirect_uri = redirect_uri
        self.non_interactive = non_interactive
        
        if token_file:
            self.token_file = token_file
        else:
            token_env = os.getenv("WHOOP_TOKEN_FILE")
            if token_env:
                self.token_file = token_env
            else:
                repo_root = Path(__file__).resolve().parent.parent
                self.token_file = str(repo_root / "data" / "whoop_tokens.json")
        
        self.oauth_base_url = "https://api.prod.whoop.com"
        self.api_base_url = "https://api.prod.whoop.com/developer"
        self.scopes = "offline read:recovery read:sleep read:workout read:cycles read:profile read:body_measurement"
        
    def _load_tokens(self) -> Optional[Dict[str, Any]]:
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as f:
                return json.load(f)
        return None
    
    def _save_tokens(self, tokens: Dict[str, Any]) -> None:
        os.makedirs(os.path.dirname(self.token_file) or '.', exist_ok=True)
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            dir=os.path.dirname(self.token_file) or '.',
            delete=False
        )
        try:
            json.dump(tokens, temp_file, indent=2)
            temp_file.close()
            os.replace(temp_file.name, self.token_file)
        except Exception:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
            raise
    
    def authorize(self) -> str:
        state = secrets.token_urlsafe(32)
        self._state = state
        
        auth_url = (
            f"{self.oauth_base_url}/oauth/oauth2/auth?"
            f"response_type=code&client_id={self.client_id}&"
            f"redirect_uri={urllib.parse.quote(self.redirect_uri)}&"
            f"scope={urllib.parse.quote(self.scopes)}&"
            f"state={state}"
        )
        print("\n" + "="*60)
        print("WHOOP AUTHORIZATION REQUIRED")
        print("="*60)
        print("\nOpen this URL in your browser to authorize:")
        print(f"\n{auth_url}\n")
        
        try:
            webbrowser.open(auth_url)
            print("Browser opened automatically.\n")
        except:
            print("Could not open browser automatically. Please copy the URL above.\n")
        
        print("After approval, you'll be redirected to a URL like:")
        print(f"{self.redirect_uri}?code=XXXXX&state=XXXXX\n")
        print("Copy the 'code' parameter from that URL and paste it below.\n")
        
        return input("Enter authorization code: ").strip()
    
    def _exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        url = f"{self.oauth_base_url}/oauth/oauth2/token"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        try:
            r = requests.post(url, data=data)
            r.raise_for_status()
            tokens = r.json()
            tokens["timestamp"] = time.time()
            tokens["expires_at"] = time.time() + tokens.get("expires_in", 3600)
            self._save_tokens(tokens)
            print("\n✓ Successfully authenticated with Whoop!\n")
            return tokens
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                raise Exception("Invalid authorization code. Please try again.")
            raise Exception(f"Authentication failed: {e}")
    
    def _refresh_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        url = f"{self.oauth_base_url}/oauth/oauth2/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        try:
            r = requests.post(url, data=data)
            r.raise_for_status()
            new_tokens = r.json()
            new_tokens["timestamp"] = time.time()
            new_tokens["expires_at"] = time.time() + new_tokens.get("expires_in", 3600)
            if "refresh_token" not in new_tokens and refresh_token:
                new_tokens["refresh_token"] = refresh_token
            self._save_tokens(new_tokens)
            print("✓ Access token refreshed")
            return new_tokens
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                error_data = e.response.json() if e.response.content else {}
                if error_data.get("error") == "invalid_grant":
                    print("⚠ Refresh token revoked. Re-authorization required.")
                    if os.path.exists(self.token_file):
                        os.remove(self.token_file)
                    return None
            print(f"⚠ Token refresh failed (HTTP {e.response.status_code}). Keeping existing tokens.")
            return None
        except Exception as e:
            print(f"⚠ Token refresh error: {e}. Keeping existing tokens.")
            return None
    
    def _get_valid_token(self) -> str:
        tokens = self._load_tokens()
        if not tokens:
            if self.non_interactive:
                raise Exception(
                    "No authentication token found. Run the following command manually to authenticate:\n"
                    f"  python {Path(__file__).resolve().parent / 'get_whoop_summary.py'}"
                )
            code = self.authorize()
            tokens = self._exchange_code_for_token(code)
        else:
            expires_at = tokens.get("expires_at", tokens.get("timestamp", 0) + 3600)
            if time.time() >= expires_at - 300:
                print("Token expired, refreshing...")
                new_tokens = self._refresh_token(tokens.get("refresh_token", ""))
                if new_tokens:
                    tokens = new_tokens
                else:
                    if self.non_interactive:
                        raise Exception(
                            "Token refresh failed. Run the following command manually to re-authenticate:\n"
                            f"  python {Path(__file__).resolve().parent / 'get_whoop_summary.py'}"
                        )
                    code = self.authorize()
                    tokens = self._exchange_code_for_token(code)
        
        return tokens["access_token"]
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        token = self._get_valid_token()
        url = f"{self.api_base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            r = requests.get(url, headers=headers, params=params)
            
            if r.status_code == 401:
                print("Token invalid, attempting refresh...")
                tokens = self._load_tokens()
                if tokens and tokens.get("refresh_token"):
                    new_tokens = self._refresh_token(tokens["refresh_token"])
                    if new_tokens:
                        token = new_tokens["access_token"]
                        headers = {"Authorization": f"Bearer {token}"}
                        r = requests.get(url, headers=headers, params=params)
                    else:
                        raise Exception("Token refresh failed. Re-authentication required.")
                else:
                    raise Exception("No refresh token available. Re-authentication required.")
            
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise Exception("Authentication failed. Token may have been revoked.")
            elif e.response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif e.response.status_code == 429:
                raise Exception("Rate limit exceeded. Please wait before retrying.")
            elif e.response.status_code >= 500:
                raise Exception(f"Whoop server error ({e.response.status_code}). Please try again later.")
            else:
                raise Exception(f"API request failed: {e}")
    
    def get_profile(self) -> Dict[str, Any]:
        return self._make_request("v1/user/profile/basic")
    
    def get_body_measurements(self) -> Dict[str, Any]:
        return self._make_request("v2/user/measurement/body")
    
    def get_recovery(
        self,
        limit: int = 10,
        start: Optional[str] = None,
        end: Optional[str] = None,
        next_token: Optional[str] = None
    ) -> Dict[str, Any]:
        params = {"limit": limit}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        if next_token:
            params["nextToken"] = next_token
        
        return self._make_request("v2/recovery", params)
    
    def get_recovery_for_cycle(self, cycle_id: int) -> Dict[str, Any]:
        return self._make_request(f"v2/recovery/cycle/{cycle_id}")
    
    def get_sleep(
        self,
        limit: int = 10,
        start: Optional[str] = None,
        end: Optional[str] = None,
        next_token: Optional[str] = None
    ) -> Dict[str, Any]:
        params = {"limit": limit}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        if next_token:
            params["nextToken"] = next_token
        
        return self._make_request("v2/activity/sleep", params)
    
    def get_sleep_by_id(self, sleep_id: str) -> Dict[str, Any]:
        return self._make_request(f"v2/activity/sleep/{sleep_id}")
    
    def get_workouts(
        self,
        limit: int = 10,
        start: Optional[str] = None,
        end: Optional[str] = None,
        next_token: Optional[str] = None
    ) -> Dict[str, Any]:
        params = {"limit": limit}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        if next_token:
            params["nextToken"] = next_token
        
        return self._make_request("v2/activity/workout", params)
    
    def get_workout_by_id(self, workout_id: str) -> Dict[str, Any]:
        return self._make_request(f"v2/activity/workout/{workout_id}")
    
    def get_cycles(
        self,
        limit: int = 10,
        start: Optional[str] = None,
        end: Optional[str] = None,
        next_token: Optional[str] = None
    ) -> Dict[str, Any]:
        params = {"limit": limit}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        if next_token:
            params["nextToken"] = next_token
        
        return self._make_request("v2/cycle", params)
    
    def get_cycle_by_id(self, cycle_id: int) -> Dict[str, Any]:
        return self._make_request(f"v2/cycle/{cycle_id}")
    
    def get_sleep_for_cycle(self, cycle_id: int) -> Dict[str, Any]:
        return self._make_request(f"v2/cycle/{cycle_id}/sleep")
    
    def revoke_access(self) -> None:
        token = self._get_valid_token()
        url = f"{self.api_base_url}/v2/user/access"
        headers = {"Authorization": f"Bearer {token}"}
        
        r = requests.delete(url, headers=headers)
        r.raise_for_status()
        
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
        
        print("✓ Access revoked successfully")
