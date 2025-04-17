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
        return redirect(url_for('onboarding.index'))
    
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