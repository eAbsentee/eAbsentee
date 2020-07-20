import os
import sys
from flask_login import UserMixin
from ..app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))

class AdminUser(db.Model, UserMixin):
    """Data model for voters and their information."""

    __tablename__ = 'new_admin_users'

    id = db.Column(db.Integer, primary_key=True) # ID
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False, unique=False)


    def __repr__(self):
        return '<User {}>'.format(self.username)
