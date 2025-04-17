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
    
    def get_questionnaire_sections(self):
        """Get all questionnaire sections from the API."""
        try:
            response = requests.get(f"{self.base_url}/questionnaire/sections")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error fetching questionnaire sections: {e}")
            # Return default sections if API is unavailable
            raise e
    
    def get_questionnaire_by_section(self, section):
        """Get questionnaire data for a specific section from the API."""
        try:
            response = requests.get(f"{self.base_url}/questionnaire/section/{section}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error fetching questionnaire for section {section}: {e}")
            # Return None if API is unavailable
            raise e
    
    def submit_responses(self, responses):
        """Submit questionnaire responses to the API."""
        try:
            response = requests.post(f"{self.base_url}/questionnaire/submit", json=responses)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error submitting responses: {e}")
            raise e

# Create a singleton instance
api_client = PsychologyServiceClient() 