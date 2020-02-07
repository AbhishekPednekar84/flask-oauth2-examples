from flask import Flask
from utilities.db import db
from utilities.login_manager import login_manager
from config import Config

login_manager.login_view = "login"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints
    from routes.home_view import home_bp
    from routes.login_views import login_bp
    from routes.google_oauth import google_oauth_bp
    from routes.github_oauth import github_oauth_bp
    from routes.linkedin_oauth import linkedin_oauth_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(google_oauth_bp)
    app.register_blueprint(github_oauth_bp)
    app.register_blueprint(linkedin_oauth_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(ssl_context="adhoc", debug=True)
