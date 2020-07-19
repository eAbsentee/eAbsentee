import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from eAbsentee.config import Config


load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    sys.path.append(os.path.join(os.path.dirname(__file__)))
    with app.app_context():
        from eAbsentee.form.models import User

        db.create_all()

        from eAbsentee.form import form
        # from eAbsentee.home import home
        from eAbsentee.admin import admin

        app.register_blueprint(form.form_bp)
        app.register_blueprint(home.home_bp)
        app.register_blueprint(admin.admin_bp)

        return app
