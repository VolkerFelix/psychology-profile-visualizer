"""
Questionnaire model that fetches data from the psychology-service API.
"""
from app.utils.api_client import api_client
from flask import current_app

def get_all_sections():
    """Get all questionnaire sections from the API."""
    try:
        # For now, return a static list of sections that match our questionnaire types
        return ['personality', 'sleep', 'behavioral']
    except Exception as e:
        current_app.logger.error(f"Error getting sections: {e}")
        raise e
    
def get_questionnaire_by_section(section):
    """
    Get questions for a specific section of the questionnaire from the API.
    
    Args:
        section (str): The section name ('personality', 'sleep', or 'behavioral')
        
    Returns:
        dict: A dictionary with section info and questions
    """
    try:
        # Map frontend sections to backend questionnaire types
        section_to_type = {
            'personality': 'personality',
            'sleep': 'sleep_habits',
            'behavioral': 'behavioral'
        }
        
        questionnaire_type = section_to_type.get(section)
        if not questionnaire_type:
            raise ValueError(f"Invalid section: {section}")
            
        # Get the questionnaire for this type
        questionnaire = api_client.get_questionnaire_by_type(questionnaire_type)
        
        # Transform the response to match the frontend's expected format
        return {
            'section': section,
            'title': questionnaire.get('title', ''),
            'description': questionnaire.get('description', ''),
            'questions': questionnaire.get('questions', [])
        }
        
    except Exception as e:
        current_app.logger.error(f"Error getting questionnaire for section {section}: {e}")
        raise e