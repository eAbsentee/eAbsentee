import os, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__)))

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    set_config(app)
    init_apps(app)
    with app.app_context():
        database_models(db)
        register_blueprints(app)
        return app

def set_config(app):
    from eAbsentee.config import Config
    app.config.from_object(Config)

def init_apps(app):
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    login_manager.login_view = 'login'
    migrate = Migrate(app, db)

def database_models(db):
    from eAbsentee.form.models import User
    from eAbsentee.admin.models import AdminUser
    if os.environ['TESTING_MODE']:
        db.create_all()

def register_blueprints(app):
    from eAbsentee.form import form
    from eAbsentee.home import home
    from eAbsentee.admin import admin

    app.register_blueprint(form.form_bp)
    app.register_blueprint(home.home_bp)
    app.register_blueprint(admin.admin_bp)
