import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from application.config import Config


load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from application.form.models import User

        db.create_all()

        from application.form import form
        from application.home import home
        from application.admin import admin

        app.register_blueprint(form.form_bp)
        app.register_blueprint(home.home_bp)
        app.register_blueprint(admin.admin_bp)

        return app
