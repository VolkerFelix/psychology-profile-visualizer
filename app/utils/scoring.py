"""
Scoring logic for questionnaires to generate psychological profiles.
"""
from app.models.profile import PsychologicalProfile
from app.models.questionnaire import get_questionnaire_by_section

def score_responses(responses):
    """
    Score questionnaire responses and generate a psychological profile.
    
    Args:
        responses (dict): Dictionary of question IDs to response values
        
    Returns:
        dict: Psychological profile as a dictionary
    """
    # Initialize scores for each dimension
    personality_scores = {
        'openness': 0,
        'conscientiousness': 0,
        'extraversion': 0,
        'agreeableness': 0,
        'neuroticism': 0
    }
    personality_counts = {dim: 0 for dim in personality_scores}
    
    sleep_preferences = {
        'chronotype': None,
        'ideal_bedtime': None,
        'environment_preference': None,
        'sleep_anxiety_level': 0,
        'relaxation_techniques': []
    }
    
    behavioral_patterns = {
        'stress_response': None,
        'routine_consistency': 0,
        'exercise_frequency': 0,
        'social_activity_preference': 0,
        'screen_time_before_bed': 0
    }
    
    # Get all questions from all sections
    all_questions = {}
    for section in ['personality', 'sleep', 'behavioral']:
        section_data = get_questionnaire_by_section(section)
        for question in section_data['questions']:
            all_questions[question['id']] = question
    
    # Process each response
    for question_id, response_value in responses.items():
        if question_id not in all_questions:
            continue
            
        question = all_questions[question_id]
        dimension = question.get('dimension', '')
        
        # Process personality traits (using Likert scale)
        if dimension in personality_scores:
            if question['type'] == 'likert_5':
                # Convert Likert 1-5 to 0-100 scale
                score = (int(response_value) - 1) * 25
                personality_scores[dimension] += score
                personality_counts[dimension] += 1
        
        # Process sleep preferences
        elif dimension == 'chronotype':
            # Get the selected option's value
            for option in question['options']:
                if option['id'] == response_value:
                    sleep_preferences['chronotype'] = option['value']
                    break
        
        elif dimension == 'sleep_environment':
            # Get the selected option's value
            for option in question['options']:
                if option['id'] == response_value:
                    sleep_preferences['environment_preference'] = option['value']
                    break
        
        elif dimension == 'sleep_anxiety':
            # Slider from 0-10
            sleep_preferences['sleep_anxiety_level'] = int(response_value)
        
        elif dimension == 'ideal_bedtime':
            sleep_preferences['ideal_bedtime'] = response_value
        
        elif dimension == 'relaxation_techniques':
            # Checkbox question, response is a list of selected options
            if isinstance(response_value, str):
                if ',' in response_value:
                    # Handle case where response is comma-separated string
                    selected_ids = [id.strip() for id in response_value.split(',')]
                else:
                    # Single selection
                    selected_ids = [response_value]
            else:
                # Already a list
                selected_ids = response_value
            
            # Get the values for selected options
            techniques = []
            for option in question['options']:
                if option['id'] in selected_ids and option['id'] != 'none':
                    techniques.append(option['value'])
            
            sleep_preferences['relaxation_techniques'] = techniques
        
        # Process behavioral patterns
        elif dimension == 'stress_response':
            # Get the selected option's value
            for option in question['options']:
                if option['id'] == response_value:
                    behavioral_patterns['stress_response'] = option['value']
                    break
        
        elif dimension == 'routine_consistency':
            # Slider from 0-10
            behavioral_patterns['routine_consistency'] = int(response_value)
        
        elif dimension == 'exercise_frequency':
            # Slider from 0-7
            behavioral_patterns['exercise_frequency'] = int(response_value)
        
        elif dimension == 'social_activity_preference':
            # Slider from 0-10
            behavioral_patterns['social_activity_preference'] = int(response_value)
        
        elif dimension == 'screen_time_before_bed':
            # Slider from 0-120
            behavioral_patterns['screen_time_before_bed'] = int(response_value)
    
    # Calculate average scores for personality dimensions
    for dimension in personality_scores:
        if personality_counts[dimension] > 0:
            personality_scores[dimension] = round(personality_scores[dimension] / personality_counts[dimension])
        else:
            personality_scores[dimension] = 50  # Default middle value
    
    # Create and return the psychological profile
    profile = PsychologicalProfile(
        personality_traits=personality_scores,
        sleep_preferences=sleep_preferences,
        behavioral_patterns=behavioral_patterns
    )
    
    return profile.to_dict()