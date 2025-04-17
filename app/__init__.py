from flask import Flask
from config import config
import os

def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Register blueprints
    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.routes.onboarding import onboarding as onboarding_blueprint
    app.register_blueprint(onboarding_blueprint)

    from app.routes.profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    return app