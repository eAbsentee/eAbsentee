import os
import sys
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__)))

from ..app import db

class User(db.Model):
    """Data model for voters and their information."""

    __tablename__ = 'users'

    application_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128), index=False, nullable=False)
    county = db.Column(db.String(128), index=False, nullable=False)
    submission_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email = db.Column(db.String(128), index=False)
    phonenumber = db.Column(db.String(128), index=False)
    full_address = db.Column(db.String(256), index=False, nullable=False)
    ip = db.Column(db.String(128), index=False, nullable=False)
    group_code = db.Column(db.String(128), index=False)

    def __repr__(self):
        return '<Voter {}>'.format(self.name)
