from flask import Blueprint, logging, render_template, request, session, redirect, url_for, jsonify, flash
from app.models.questionnaire import get_questionnaire_by_section, get_all_sections
from app.utils.scoring import score_responses
from app.utils.api_client import api_client
import uuid

onboarding = Blueprint('onboarding', __name__, url_prefix='/onboarding')

@onboarding.route('/', methods=['GET'])
def index():
    """Start the onboarding process."""
    # Check if profile is already created
    if 'profile_id' not in session:
        return redirect(url_for('onboarding.create_profile'))
    
    # Initialize session if starting onboarding
    if 'current_section' not in session:
        session['current_section'] = 'personality'
        session['responses'] = {}
        session['onboarding_complete'] = False
        session['sections_completed'] = []
    
    return render_template('onboarding.html', 
                           section=session['current_section'],
                           questionnaire=get_questionnaire_by_section(session['current_section']),
                           all_sections=get_all_sections(),
                           sections_completed=session.get('sections_completed', []),
                           progress=calculate_progress())

@onboarding.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    """Create a new user profile."""
    if request.method == 'POST':
        # Get form data and store in session for later use
        session['user_data'] = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'age': int(request.form.get('age')),
            'gender': request.form.get('gender'),
            'occupation': request.form.get('occupation'),
            'timezone': request.form.get('timezone')
        }
        
        # Create profile data matching the backend model
        profile_data = {
            'user_id': str(uuid.uuid4()),  # Generate a unique ID
            'personality_traits': None,
            'sleep_preferences': None,
            'behavioral_patterns': None,
            'raw_scores': None
        }
        
        try:
            # Create profile in the API
            profile_result = api_client.create_profile(profile_data)
            
            # Store profile ID and user data in session
            session['profile_id'] = profile_result.get('profile', {}).get('profile_id')
            session['profile_data'] = profile_result
            
            # Redirect to the first section
            return redirect(url_for('onboarding.index'))
            
        except Exception as e:
            current_app.logger.error(f"Error creating profile: {e}")
            flash('Error creating profile. Please try again.', 'error')
            return redirect(url_for('onboarding.create_profile'))
    
    return render_template('create_profile.html')

@onboarding.route('/submit', methods=['POST'])
def submit_section():
    """Submit answers for the current section."""
    # Check if profile exists
    if 'profile_id' not in session:
        return redirect(url_for('onboarding.create_profile'))
    
    data = request.form.to_dict()
    current_section = session['current_section']
    
    # Store responses in session
    if 'responses' not in session:
        session['responses'] = {}
    
    # Extract responses from form data
    for key, value in data.items():
        if key.startswith('question_'):
            question_id = key.replace('question_', '')
            session['responses'][question_id] = value
    
    # Mark current section as completed
    if current_section not in session.get('sections_completed', []):
        sections_completed = session.get('sections_completed', [])
        sections_completed.append(current_section)
        session['sections_completed'] = sections_completed
    
    # Determine next section
    all_sections = get_all_sections()
    current_index = all_sections.index(current_section)
    
    if current_index < len(all_sections) - 1:
        # Move to next section
        session['current_section'] = all_sections[current_index + 1]
        return redirect(url_for('onboarding.index'))
    else:
        # All sections completed
        session['onboarding_complete'] = True
        
        # Submit responses to the API
        api_result = api_client.submit_responses(session['responses'])
        
        if api_result:
            # Use the profile from the API if available
            session['profile'] = api_result
        else:
            raise Exception("API is unavailable")
        
        # Redirect to profile page
        return redirect(url_for('profile.index'))

@onboarding.route('/section/<section_name>', methods=['GET'])
def goto_section(section_name):
    """Go to a specific section of the questionnaire."""
    # Check if profile exists
    if 'profile_id' not in session:
        return redirect(url_for('onboarding.create_profile'))
    
    all_sections = get_all_sections()
    
    if section_name in all_sections:
        session['current_section'] = section_name
    
    return redirect(url_for('onboarding.index'))

def calculate_progress():
    """Calculate progress percentage through onboarding."""
    all_sections = get_all_sections()
    completed = len(session.get('sections_completed', []))
    total = len(all_sections)
    
    if total == 0:
        return 0
    
    return int((completed / total) * 100)