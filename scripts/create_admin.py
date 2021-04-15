from sys import path
path.append("../eAbsentee")

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
from eAbsentee.admin.models import AdminUser, ACCESS
from flask_bcrypt import Bcrypt
from getpass import getpass


# untested on prod DB (PythonAnywhere probably requires SSH tunneling)
engine = create_engine(getenv("SQLALCHEMY_DATABASE_URI"))
Session = sessionmaker(engine)

with Session() as session:
    email = input("Enter the new admin's email: ")
    raw_password = getpass("Enter the new admin's password: ")
    new_admin = AdminUser(
        email=email,
        password=Bcrypt().generate_password_hash(raw_password).decode('utf-8'),
        access=ACCESS["admin"],
    )
    session.add(new_admin)
    session.commit()
