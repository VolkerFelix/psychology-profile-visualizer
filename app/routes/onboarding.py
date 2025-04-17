from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, flash
from app.models.questionnaire import get_questionnaire_by_section, get_all_sections
from app.utils.scoring import score_responses

onboarding = Blueprint('onboarding', __name__, url_prefix='/onboarding')

@onboarding.route('/', methods=['GET'])
def index():
    """Start the onboarding process."""
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

@onboarding.route('/submit', methods=['POST'])
def submit_section():
    """Submit answers for the current section."""
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
        
        # Score responses and generate profile
        profile = score_responses(session['responses'])
        session['profile'] = profile
        
        # Redirect to profile page
        return redirect(url_for('profile.index'))

@onboarding.route('/section/<section_name>', methods=['GET'])
def goto_section(section_name):
    """Go to a specific section of the questionnaire."""
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