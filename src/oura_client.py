import os
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, Any


class OuraClient:
    """
    Oura Ring API client using Personal Access Token authentication.
    
    This client provides access to Oura Ring's v2 API endpoints for personal info,
    sleep, readiness, activity, SpO2, and heart rate data.
    """
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize the Oura API client.
        
        Args:
            access_token: Personal Access Token from Oura developer dashboard
        """
        load_dotenv()
        self.access_token = access_token or os.getenv("OURA_ACCESS_TOKEN")
        self.api_base_url = "https://api.ouraring.com"
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make an authenticated request to the Oura API.
        
        Args:
            endpoint: API endpoint (e.g., 'v2/usercollection/personal_info')
            params: Optional query parameters
            
        Returns:
            dict: JSON response from the API
            
        Raises:
            Exception: If the request fails
        """
        url = f"{self.api_base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            r = requests.get(url, headers=headers, params=params)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise Exception("Authentication failed. Invalid or expired access token.")
            elif e.response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif e.response.status_code == 429:
                raise Exception("Rate limit exceeded. Please wait before retrying.")
            elif e.response.status_code >= 500:
                raise Exception(f"Oura server error ({e.response.status_code}). Please try again later.")
            else:
                raise Exception(f"API request failed: {e}")
    
    def get_personal_info(self) -> Dict[str, Any]:
        """
        Get user's personal information.
        
        Returns:
            dict: Personal info including age, weight, height, biological_sex, email
            
        Example response:
            {
                "id": "8f9a5221-639e-4a85-81cb-4065ef23f979",
                "age": 31,
                "weight": 74.8,
                "height": 1.8,
                "biological_sex": "male",
                "email": "example@example.com"
            }
        """
        return self._make_request("v2/usercollection/personal_info")
    
    def get_sleep(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 1
    ) -> Dict[str, Any]:
        """
        Get sleep data with actual duration values (not scores).
        
        Args:
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)
            limit: Not used by Oura API but kept for consistency with WHOOP pattern
            
        Returns:
            dict: Sleep data with actual durations in seconds, averages, and percentages
            
        Example response:
            {
                "data": [{
                    "id": "string",
                    "day": "2022-09-01",
                    "total_sleep_duration": 25230,
                    "deep_sleep_duration": 4200,
                    "light_sleep_duration": 18750,
                    "rem_sleep_duration": 2280,
                    "awake_time": 3600,
                    "latency": 540,
                    "efficiency": 85,
                    "average_breath": 15,
                    "average_heart_rate": 58
                }]
            }
        """
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        return self._make_request("v2/usercollection/sleep", params)
    
    def get_daily_readiness(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 1
    ) -> Dict[str, Any]:
        """
        Get daily readiness scores.
        
        Args:
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)
            limit: Not used by Oura API but kept for consistency with WHOOP pattern
            
        Returns:
            dict: Daily readiness data with scores and contributors
            
        Example response:
            {
                "data": [{
                    "id": "string",
                    "day": "2021-10-27",
                    "score": 66,
                    "temperature_deviation": -0.2,
                    "temperature_trend_deviation": 0.1,
                    "timestamp": "2021-10-27T00:00:00+00:00",
                    "contributors": {
                        "activity_balance": 56,
                        "body_temperature": 98,
                        "hrv_balance": 75,
                        "previous_day_activity": null,
                        "previous_night": 35,
                        "recovery_index": 47,
                        "resting_heart_rate": 94,
                        "sleep_balance": 73
                    }
                }]
            }
        """
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        return self._make_request("v2/usercollection/daily_readiness", params)
    
    def get_daily_activity(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 1
    ) -> Dict[str, Any]:
        """
        Get daily activity data.
        
        Args:
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)
            limit: Not used by Oura API but kept for consistency with WHOOP pattern
            
        Returns:
            dict: Daily activity data with scores, steps, calories, and contributors
            
        Example response:
            {
                "data": [{
                    "id": "8f9a5221-639e-4a85-81cb-4065ef23f979",
                    "score": 82,
                    "active_calories": 1222,
                    "average_met_minutes": 1.90625,
                    "contributors": {
                        "meet_daily_targets": 43,
                        "move_every_hour": 100,
                        "recovery_time": 100,
                        "stay_active": 98,
                        "training_frequency": 71,
                        "training_volume": 98
                    },
                    "equivalent_walking_distance": 20122,
                    "high_activity_met_minutes": 444,
                    "high_activity_time": 3000,
                    "steps": 18430,
                    "total_calories": 3446,
                    "day": "2021-11-26",
                    "timestamp": "2021-11-26T04:00:00-08:00"
                }]
            }
        """
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        return self._make_request("v2/usercollection/daily_activity", params)
    
    def get_daily_spo2(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 1
    ) -> Dict[str, Any]:
        """
        Get daily SpO2 (blood oxygen saturation) data.
        
        Args:
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)
            limit: Not used by Oura API but kept for consistency with WHOOP pattern
            
        Returns:
            dict: Daily SpO2 data
            
        Example response:
            {
                "data": [{
                    "id": "8f9a5221-639e-4a85-81cb-4065ef23f979",
                    "day": "2019-08-24",
                    "spo2_percentage": {
                        "average": 95
                    }
                }]
            }
        """
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        return self._make_request("v2/usercollection/daily_spo2", params)
    
    def get_heartrate(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 1
    ) -> Dict[str, Any]:
        """
        Get heart rate data.
        
        Note: Heart rate endpoint uses datetime parameters internally, but this method
        accepts date strings for consistency with other methods. If you need more
        precise datetime filtering, use start_datetime and end_datetime parameters
        directly with _make_request().
        
        Args:
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)
            limit: Not used by Oura API but kept for consistency with WHOOP pattern
            
        Returns:
            dict: Heart rate data with timestamps
            
        Example response:
            {
                "data": [{
                    "bpm": 60,
                    "source": "sleep",
                    "timestamp": "2021-01-01T01:02:03+00:00"
                }]
            }
        """
        params = {}
        if start_date:
            params["start_datetime"] = f"{start_date}T00:00:00+00:00"
        if end_date:
            params["end_datetime"] = f"{end_date}T23:59:59+00:00"
        
        return self._make_request("v2/usercollection/heartrate", params)
    
    def get_heart_rate(
        self,
        start_datetime: Optional[str] = None,
        end_datetime: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get heart rate data with datetime precision.
        
        Args:
            start_datetime: Start datetime in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
            end_datetime: End datetime in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
            
        Returns:
            dict: Heart rate measurements with timestamps
        """
        params = {}
        if start_datetime:
            params["start_datetime"] = start_datetime
        if end_datetime:
            params["end_datetime"] = end_datetime
        
        return self._make_request("v2/usercollection/heartrate", params)
    
    def get_workouts(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get workout data.
        
        Args:
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)
            
        Returns:
            dict: Workout sessions with heart rate data, intensity, and duration
        """
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        return self._make_request("v2/usercollection/workout", params)
    
    def get_daily_stress(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get daily stress data (requires Gen3 ring).
        
        Args:
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)
            
        Returns:
            dict: Daily stress summaries
        """
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        return self._make_request("v2/usercollection/daily_stress", params)
    
    def get_tags(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get user-created tags for tracking habits, activities, symptoms.
        
        Args:
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)
            
        Returns:
            dict: User tags with timestamps
        """
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        return self._make_request("v2/usercollection/tag", params)
    
    def get_ring_configuration(self) -> Dict[str, Any]:
        """
        Get ring hardware details and configuration.
        
        Returns:
            dict: Ring configuration including hardware version and settings
        """
        return self._make_request("v2/usercollection/ring_configuration")
