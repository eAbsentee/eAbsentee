import os
import sys
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..app import db, login_manager

# sys.path.append(os.path.join(os.path.dirname(__file__)))
@login_manager.user_loader
class AdminUser(UserMixin, db.Model):
    """Data model for voters and their information."""

    __tablename__ = 'admin_users'

    id = db.Column(db.String(128), primary_key=True, unique=True) # email
    password = db.Column(db.String(256), index=False, nullable=False, unique=False)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


    def __repr__(self):
        return '<User {}>'.format(self.username)
