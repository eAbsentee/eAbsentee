"""
This script is a scheduled call to the remind web endpoint. That endpoint emails group heads who have had their group code used in the past 24 hours with a reminder email to check the dashboard. You can follow through the code in the admin blueprint.

This script should be scheduled daily.
"""

import os
from sys import path
path.append("../eAbsentee")
import requests
import csv
import sshtunnel
from os import environ, path
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from eAbsentee.form.models import db, User
from string import ascii_lowercase, digits
from random import choices as random_choices
load_dotenv()

application_id_chars = ascii_lowercase + digits

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0
host = '127.0.0.1'
user = os.environ["PA_USER"]
passwd = os.environ["PA_DB_PWD"]
db = os.environ["PA_DB"]

# This SSH is configured for the PythonAnywhere host
with sshtunnel.SSHTunnelForwarder(
    ('ssh.pythonanywhere.com'),
    ssh_password=os.environ["SSH_PWD"],
    ssh_username=os.environ["PA_USER"],
    remote_bind_address=(str(os.environ["PA_USER"] + '.mysql.pythonanywhere-services.com'), 3306)
) as server:
    print('Server connected via SSH')
    port = str(server.local_bind_port)
    conn_addr = 'mysql://' + user + ':' + passwd + '@' + host + ':' + port + '/' + db
    engine = create_engine(conn_addr, pool_recycle=280)
    Base = declarative_base()
    Base.metadata.bind = engine
    Session = sessionmaker(bind=engine)
    session = Session()

    new_voter = User(
        application_id = ''.join(random_choices(application_id_chars, k=24)),
        name='TEST NAME',
        county='TEST COUNTY',
        email='testing@eabsentee.org',
        phonenumber='',
        full_address='',
        ip='',
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
