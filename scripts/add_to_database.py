import csv
import os
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

    filename = 'INSERT'

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        for row in csvreader:
            from dateutil import parser
            new_voter = User(
                application_id=row[0],
                name=row[1],
                submission_time=parser.parse(row[3]),
                county=row[2],
                email=row[4],
                phonenumber=row[5],
                full_address=row[6],
                ip=row[7],
                group_code=row[8],
                lat=row[9],
                long=row[10]
            )

            session.add(new_voter)
            session.commit()
