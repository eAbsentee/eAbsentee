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
    from dateutil import parser
    filename = 'INSERT'

    with open(filename, 'r', encoding='cp1252') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            new_voter = User(
                application_id=row[0],
                name=row[1],
                county=row[2],
                submission_time=parser.parse(row[3]),
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

add_to_database_all_voters()
