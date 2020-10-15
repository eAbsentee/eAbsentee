import os
import sys
from flask_login import UserMixin
from eAbsentee.app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(user_id)

ACCESS = {
    'guest': 0,
    'admin': 1,
}

class AdminUser(db.Model, UserMixin):
    """Data model for voters and their information."""

    __tablename__ = 'admin_user'

    id = db.Column(db.Integer, primary_key=True) # ID
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False, unique=False)
    access = db.Column(db.Integer, nullable=False, unique=False)


    def __repr__(self):
        return '<User {}>'.format(self.email)

    def is_admin(self):
        return self.access == ACCESS['admin']

class GroupReference(db.Model):
    """Data model for admin user to list of emails"""

    __tablename__ = 'group_references'

    id = db.Column(db.Integer(), primary_key=True) # ID PK
    email = db.Column(db.String(128)) # Email from AdminUser
    group_code = db.Column(db.String(128))

    def __repr__(self):
        return '<Email ' + self.email + ', Group Code ' + self.group_code + '>'

class RegisterLink(db.Model):
    """Currently created register links"""

    __tablename__ = 'register_links'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(32), nullable=False, unique=True)

    def __repr__(self):
        return '<RegisterLink {}>'.format(self.link)
