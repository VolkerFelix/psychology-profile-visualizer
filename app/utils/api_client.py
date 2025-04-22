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
    
    def submit_responses(self, responses, user_id=None):
        """Submit questionnaire responses to the API."""
        try:
            # Get user_id from the responses if not provided
            if not user_id and 'user_id' in responses:
                user_id = responses['user_id']
            
            # Log the responses for debugging
            current_app.logger.info(f"Processing responses for user ID: {user_id}")
            
            # 1. Get questionnaire data to understand question types and proper ranges
            questionnaires_response = requests.get(
                f"{self.base_url}/questionnaires/",
                params={"questionnaire_type": "onboarding", "is_active": "true"}
            )
            questionnaires_response.raise_for_status()
            questionnaires_data = questionnaires_response.json()
            
            if not questionnaires_data.get('questionnaires'):
                raise Exception("No active onboarding questionnaires found")
                
            questionnaire_id = questionnaires_data['questionnaires'][0]['questionnaire_id']
            
            # Extract question information for proper value processing
            question_info = {}
            for question in questionnaires_data['questionnaires'][0].get('questions', []):
                q_id = question.get('question_id')
                q_info = {
                    'type': question.get('question_type'),
                    'dimensions': question.get('dimensions', []),
                    'min_value': question.get('min_value'),
                    'max_value': question.get('max_value')
                }
                question_info[q_id] = q_info
            
            # 2. Start the questionnaire for the user
            start_response = requests.post(
                f"{self.base_url}/questionnaires/start",
                params={"questionnaire_id": questionnaire_id, "user_id": user_id}
            )
            start_response.raise_for_status()
            start_data = start_response.json()
            
            if 'questionnaire' not in start_data:
                raise Exception("Failed to start questionnaire session")
                
            user_questionnaire_id = start_data['questionnaire']['user_questionnaire_id']
            
            # 3. Process and submit the answers
            answers = []
            for question_id, value in responses.items():
                if question_id.startswith('question_'):
                    actual_id = question_id.replace('question_', '')
                    q_info = question_info.get(actual_id, {})
                    
                    # Process the value based on question type and expected ranges
                    processed_value = self._process_value(value, q_info)
                    
                    answers.append({
                        "question_id": actual_id,
                        "value": processed_value
                    })
                    
                    current_app.logger.info(f"Processed question {actual_id}: {value} → {processed_value}")
            
            answer_submission = {
                "questionnaire_id": questionnaire_id,
                "user_id": user_id,
                "answers": answers
            }
            
            submit_response = requests.post(
                f"{self.base_url}/questionnaires/answer",
                json=answer_submission
            )
            submit_response.raise_for_status()
            
            # 4. Get the current profile to check values before completion
            profile_response = requests.get(
                f"{self.base_url}/profiles/user/{user_id}"
            )
            profile_response.raise_for_status()
            profile_data = profile_response.json().get('profile', {})
            
            current_app.logger.info(f"Current profile data before completion: {profile_data}")
            
            # 5. Complete the questionnaire
            complete_response = requests.post(
                f"{self.base_url}/questionnaires/complete/{user_questionnaire_id}"
            )
            complete_response.raise_for_status()
            
            # 6. Get the final updated profile
            final_profile_response = requests.get(
                f"{self.base_url}/profiles/user/{user_id}"
            )
            final_profile_response.raise_for_status()
            
            # Return the complete profile data
            return final_profile_response.json().get('profile')
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error submitting responses: {e}")
            if hasattr(e, 'response') and e.response:
                try:
                    error_detail = e.response.json()
                    current_app.logger.error(f"API Error details: {error_detail}")
                except:
                    current_app.logger.error(f"API Error status code: {e.response.status_code}")
                    current_app.logger.error(f"API Error response: {e.response.text}")
            raise e

    def _process_value(self, value, question_info):
        """Process a value based on question type and constraints."""
        q_type = question_info.get('type')
        dimensions = question_info.get('dimensions', [])
        min_val = question_info.get('min_value')
        max_val = question_info.get('max_value')
        
        # Handle slider questions with numerical constraints
        if q_type == 'slider' and min_val is not None and max_val is not None:
            try:
                val = float(value)
                # Ensure value is within allowed range
                val = min(max_val, max(min_val, val))
                return val
            except (ValueError, TypeError):
                # If conversion fails, return original value
                return value
        
        # Handle social_activity_preference specifically
        dimension_str = str(dimensions)
        if 'social_activity_preference' in dimension_str:
            try:
                val = float(value)
                return min(10, max(0, val))
            except (ValueError, TypeError):
                return value
        
        # Handle checkbox questions
        if q_type == 'checkbox' and isinstance(value, str) and ',' in value:
            return value.split(',')
        
        # Default: return original value
        return value

        def _process_question_value(self, question_id, value):
            """Process the question value based on the question type."""
            # Handle social_activity_preference - scale back to 0-10
            if question_id == 'social_preference':
                try:
                    # Convert to float and ensure it's in the 0-10 range
                    return min(10, max(0, float(value)))
                except (ValueError, TypeError):
                    return 5  # Default value
            
            # Handle routine_consistency - scale back to 0-10
            if question_id == 'routine_consistency':
                try:
                    return min(10, max(0, float(value)))
                except (ValueError, TypeError):
                    return 5
            
            # Handle exercise_frequency - scale back to 0-7
            if question_id == 'exercise_frequency':
                try:
                    return min(7, max(0, float(value)))
                except (ValueError, TypeError):
                    return 3
            
            # Handle sleep_anxiety - scale back to 0-10
            if question_id == 'sleep_anxiety':
                try:
                    return min(10, max(0, float(value)))
                except (ValueError, TypeError):
                    return 5
            
            # Handle checkbox values
            if question_id == 'bedtime_routine' and ',' in value:
                return [v.strip() for v in value.split(',')]
            
            # Return the original value for other questions
            return value

# Create a singleton instance
api_client = PsychologyServiceClient() 