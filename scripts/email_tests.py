"""
This script is a scheduled call to the remind web endpoint. That endpoint emails group heads who have had their group code used in the past 24 hours with a reminder email to check the dashboard. You can follow through the code in the admin blueprint.

This script should be scheduled daily.
"""

import os
import requests
from os import environ, path
from datetime import datetime
from random import choices as random_choices
from string import ascii_lowercase, digits

from sys import path
path.append("../eAbsentee")

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, Column, String, DateTime, asc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv
from eAbsentee.form.models import db, User
from flask_bcrypt import Bcrypt
from getpass import getpass

application_id_chars = ascii_lowercase + digits

engine = create_engine(getenv("SQLALCHEMY_DATABASE_URI"))
Session = sessionmaker(engine)

with Session() as session:
    new_voter = User(
        application_id = ''.join(random_choices(application_id_chars, k=24)),
        name='TEST NAME',
        county='TEST COUNTY',
        email='testing@eabsentee.org',
        phonenumber='',
        full_address='',
        ip=''
        group_code='TESTING',
        lat="",
        long="",
        election_date=None,
    )

    session.add(new_voter)
    session.commit()

# TODO:
# 1) More secure storage of API key
# 2) Post URL's shouldn't be public

params = {'API_KEY': os.environ['API_KEY']}
if os.environ['FLASK_DEBUG'] == 'True':
    requests.post('http://localhost:5000/api/testing/', params=params)
else:
    requests.post('https://www.eabsentee.org/api/testing/', params=params)
