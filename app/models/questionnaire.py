"""
Questionnaire model that fetches data from the psychology-service API.
"""
from app.utils.api_client import api_client
from flask import current_app

def get_all_sections():
    """Get all questionnaire sections from the API."""
    try:
        return api_client.get_questionnaire_sections()
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
        questionnaire = api_client.get_questionnaire_by_section(section)
        return questionnaire
        
    except Exception as e:
        current_app.logger.error(f"Error getting questionnaire for section {section}: {e}")
        raise e