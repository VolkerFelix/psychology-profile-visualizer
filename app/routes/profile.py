from flask import Blueprint, render_template, session, redirect, url_for, jsonify

profile = Blueprint('profile', __name__, url_prefix='/profile')

@profile.route('/', methods=['GET'])
def index():
    """Display the psychological profile visualization."""
    # Check if onboarding is complete
    if not session.get('onboarding_complete', False):
        return redirect(url_for('onboarding.index'))
    
    # Check if profile exists
    if 'profile_id' not in session:
        return redirect(url_for('onboarding.create_profile'))
    
    # Get profile data from session
    profile_data = session.get('profile', {})
    
    if not profile_data:
        # If no profile data, redirect to onboarding
        flash("No profile data found. Please complete the questionnaire first.", "warning")
        return redirect(url_for('onboarding.index'))
    
    # Ensure top-level structures exist
    if 'personality_traits' not in profile_data:
        profile_data['personality_traits'] = {
            'openness': None,
            'conscientiousness': None,
            'extraversion': None,
            'agreeableness': None,
            'neuroticism': None,
            'dominant_traits': []
        }
    
    if 'sleep_preferences' not in profile_data:
        profile_data['sleep_preferences'] = {
            'chronotype': None,
            'ideal_bedtime': None,
            'environment_preference': None,
            'sleep_anxiety_level': None,
            'relaxation_techniques': []
        }
    
    if 'behavioral_patterns' not in profile_data:
        profile_data['behavioral_patterns'] = {
            'stress_response': None,
            'routine_consistency': None,
            'exercise_frequency': None,
            'social_activity_preference': None,
            'screen_time_before_bed': None
        }
    
    if 'overall_profile' not in profile_data:
        profile_data['overall_profile'] = {
            'insights': [],
            'strengths': [],
            'challenges': []
        }
    
    # Render profile visualization template
    return render_template('profile.html', 
                          profile=profile_data,
                          profile_id=session.get('profile_id'),
                          user_data=session.get('profile_data', {}))

@profile.route('/data', methods=['GET'])
def profile_data():
    """Return profile data as JSON for visualization."""
    # Check if profile exists
    if 'profile_id' not in session:
        return jsonify({'error': 'No profile ID available'}), 404
    
    profile_data = session.get('profile', {})
    
    if not profile_data:
        return jsonify({'error': 'No profile data available'}), 404
    
    return jsonify(profile_data)

@profile.route('/reset', methods=['GET'])
def reset():
    """Reset the profile and start over."""
    session.clear()
    return redirect(url_for('main.index'))