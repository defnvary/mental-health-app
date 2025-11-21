from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

# load user from database when needed
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize database
    db.init_app(app)
    # Initialize login_manager
    login_manager.init_app(app)

    # add auth.route for login_manager
    login_manager.login_view = 'auth.login' # type: ignore
    
    # Create tables
    with app.app_context():
        from app.models import User
        db.create_all()
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    return app