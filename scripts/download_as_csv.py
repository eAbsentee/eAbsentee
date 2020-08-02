import csv
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
load_dotenv()


Base = declarative_base()
engine = create_engine(os.environ["SQLALCHEMY_DATABASE_URI"], echo=True)
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

def add_to_database_all_voters():
    filename = 'voters.csv'

    with open(filename, 'w', encoding='cp1252', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        query = session.query(User).all()
        for user in query:
            row = [user.application_id, user.name, user.county, user.submission_time, user.email, user.phonenumber, user.full_address, user.ip, user.group_code, user.lat, user.long]
            csvwriter.writerow(row)

add_to_database_all_voters()
