"""
This script is a scheduled call to the remind web endpoint. That endpoint emails group heads who have had their group code used in the past 24 hours with a reminder email to check the dashboard. You can follow through the code in the admin blueprint.

This script should be scheduled daily.
"""

import os
import sys
import requests
import csv
import sshtunnel
from os import environ, path
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
load_dotenv()

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

    class User(Base):
        """Data model for voters and their information."""

        __tablename__ = 'users'

        application_id = Column(String(64), primary_key=True)
        name = Column(String(128), index=False, nullable=False)
        county = Column(String(128), index=False, nullable=False)
        submission_time = Column(DateTime, nullable=False, default=datetime.utcnow)
        email = Column(String(128), index=False)
        phonenumber = Column(String(128), index=False)
        full_address = Column(String(256), index=False, nullable=False)
        ip = Column(String(128), index=False, nullable=False)
        group_code = Column(String(128), index=False)
        lat = Column(String(32), index=False)
        long = Column(String(32), index=False)

        def __repr__(self):
            return '<Voter {}>'.format(self.name)

        def get_address(self):
            return self.full_address

        def get_lat(self):
            return self.lat

        def get_long(self):
            return self.long

    # Create a hardcoded User instance
    new_user = User(
        application_id='123',
        name='TESTING USER',
        submission_time=datetime.utcnow(),
        county='TESTING COUNTY',
        email='testing@testing.com',
        phonenumber='1111111111',
        full_address='TESTING ADDRESS',
        ip='127.0.0.1',
        group_code='testing',
        lat='12.345',
        long='67.890'
    )

    session.add(new_user)
    session.commit()
            
    # temporary storage
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


    # TODO:
    # 1) More secure storage of API key
    # 2) Post URL's shouldn't be public

    params = {'API_KEY': os.environ['API_KEY']}
    if os.environ['FLASK_DEBUG'] == 'True':
        requests.post('http://localhost:5000/api/testing/', params=params)
    else:
        requests.post('https://www.eabsentee.org/api/testing/', params=params)
