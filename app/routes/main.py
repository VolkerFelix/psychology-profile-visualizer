from flask import Blueprint, render_template, session, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Render the landing page."""
    # Clear any existing session data if starting from the beginning
    if 'onboarding_complete' in session and not session['onboarding_complete']:
        session.clear()
    
    return render_template('index.html')