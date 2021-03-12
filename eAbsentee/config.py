import os
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Sets Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    if environ.get("FLASK_APP"):
        FLASK_APP = environ.get("FLASK_APP")

    # Automatically reloads templates upon editing of app
    TEMPLATES_AUTO_RELOAD = True
    # Sets root path of directory to actual root path
    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

    """
    SQLALCHEMY_DATABASE_URI is the database URL
    SQLALCHEMY_ECHO, SQLALCHEMY_POOL_RECYCLE, SQLALCHEMY_TRACK_MODIFICATIONS are necessary for PythonAnywhere to work
    """
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FORM_CLOSED = True
