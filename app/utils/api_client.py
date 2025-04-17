"""
API client for communicating with the psychology-service backend.
"""
import os
import requests
from flask import current_app

class PsychologyServiceClient:
    """Client for interacting with the psychology-service API."""
    
    def __init__(self, base_url=None):
        """Initialize the client with the base URL."""
        self.base_url = base_url or os.environ.get('PSYCHOLOGY_API_BASE_URL', 'http://localhost:8001/api')
    
    def get_questionnaire_by_type(self, questionnaire_type):
        """Get questionnaire data for a specific type from the API."""
        try:
            # Use the list endpoint with a filter for the questionnaire type
            response = requests.get(
                f"{self.base_url}/questionnaires/", 
                params={
                    "questionnaire_type": questionnaire_type,
                    "is_active": True,
                    "limit": 1
                }
            )
            response.raise_for_status()
            
            # Extract the first questionnaire from the response
            data = response.json()
            questionnaires = data.get('questionnaires', [])
            
            if not questionnaires:
                current_app.logger.error(f"No questionnaire found for type: {questionnaire_type}")
                return {}
                
            return questionnaires[0]
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error fetching questionnaire for type {questionnaire_type}: {e}")
            if hasattr(e.response, 'json'):
                error_detail = e.response.json()
                current_app.logger.error(f"API Error details: {error_detail}")
            raise e
    
    def create_profile(self, profile_data):
        """Create a new user profile in the API."""
        try:
            response = requests.post(f"{self.base_url}/profiles", json=profile_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error creating profile: {e}")
            if hasattr(e.response, 'json'):
                error_detail = e.response.json()
                current_app.logger.error(f"API Error details: {error_detail}")
            raise e
    
    def submit_responses(self, responses):
        """Submit questionnaire responses to the API."""
        try:
            response = requests.post(f"{self.base_url}/questionnaire/submit", json=responses)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error submitting responses: {e}")
            if hasattr(e.response, 'json'):
                error_detail = e.response.json()
                current_app.logger.error(f"API Error details: {error_detail}")
            raise e

# Create a singleton instance
api_client = PsychologyServiceClient() 