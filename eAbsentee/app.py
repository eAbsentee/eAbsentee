import os, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_talisman import Talisman
from flask_seasurf import SeaSurf
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__)))

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
# csrf = SeaSurf()
# talisman = Talisman()

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
    login_manager.login_view = 'login'
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    # csrf.init_app(app)
    # talisman.init_app(app, content_security_policy=get_csp())

def get_csp():
    return {
        'default-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            '*.cloudflare.com',
            '*.bootstrapcdn.com',
            '*.jquery.com',
            '*.googleapis.com',
            '*.gstatic.com'
        ],
        'script-src': [
            '\'self\'',
            '*.jquery.com',
            '*.googleapis.com',
            'unpkg.com',
            '*.api.smartystreets.com',
            '*.bootstrapcdn.com'
        ]
    }

def database_models(db):
    from eAbsentee.form.models import User
    from eAbsentee.admin.models import AdminUser, RegisterLink, GroupReference
    db.create_all()

def register_blueprints(app):
    from eAbsentee.form import form
    from eAbsentee.home import home
    from eAbsentee.admin import admin

    app.register_blueprint(form.form_bp)
    app.register_blueprint(home.home_bp)
    app.register_blueprint(admin.admin_bp)
