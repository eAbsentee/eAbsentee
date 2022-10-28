import os
from os import environ
from pathlib import Path
from dotenv import load_dotenv
from datetime import date
from json import load as json_load

basedir = Path(__file__).resolve().parent
load_dotenv(basedir / '.env')

class Config:
    """Sets Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_DEBUG = environ.get("FLASK_DEBUG", "false").lower() == "true"
    if environ.get("FLASK_APP"):
        FLASK_APP = environ.get("FLASK_APP")

    # Automatically reloads templates upon editing of app
    TEMPLATES_AUTO_RELOAD = True
    # Sets root path of directory to actual root path
    ROOT_PATH = basedir

    """
    SQLALCHEMY_DATABASE_URI is the database URL
    SQLALCHEMY_ECHO, SQLALCHEMY_POOL_RECYCLE, SQLALCHEMY_TRACK_MODIFICATIONS are necessary for PythonAnywhere to work
    """
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CSRF_COOKIE_SAMESITE = None
    # CSRF_CHECK_REFERER = False
    CSRF_DISABLE = True

    SESSION_COOKIE_SAMESITE = None
    # SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

    LANGUAGES = ['en', 'es']
    BABEL_TRANSLATION_DIRECTORIES = str(ROOT_PATH / "translations")

    # https://www.elections.virginia.gov/casting-a-ballot/calendars-schedules/upcoming-elections.html
    UPCOMING_ELECTIONS = [
        #date(2022, 11, 8),  # General Election
    ]
    FORM_OPEN = len(UPCOMING_ELECTIONS) > 0

    with open(basedir / 'static' / 'localities_info.json') as file:
        LOCALITIES = json_load(file)
