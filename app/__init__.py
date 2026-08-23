from flask import Flask
from config import Config
from app.extensions import db, login_manager, csrf

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Import models so SQLAlchemy knows about them
    from app.models import models

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    # Register blueprints
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.routes.students import bp as students_bp
    app.register_blueprint(students_bp, url_prefix='/students')

    from app.routes.courses import bp as courses_bp
    app.register_blueprint(courses_bp, url_prefix='/courses')

    from app.routes.attendance import bp as attendance_bp
    app.register_blueprint(attendance_bp, url_prefix='/attendance')

    from app.routes.reports import bp as reports_bp
    app.register_blueprint(reports_bp, url_prefix='/reports')

    return app
