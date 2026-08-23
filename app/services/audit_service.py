from app.extensions import db
from app.models.models import AuditLog
from flask_login import current_user

def log_action(action):
    if current_user.is_authenticated:
        log = AuditLog(user_id=current_user.id, action=action)
        db.session.add(log)
        db.session.commit()
