import os
import csv
from eAbsentee.form.models import User
from dotenv import load_dotenv
from dateutil import parser
from datetime import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

def get_users(group, date_first, date_second):
    markers = []
    date_first = parser.parse(date_first)
    date_second = parser.parse(date_second)
    for user in User.query.filter_by(group_code=group).filter(User.submission_time >= date_first).filter(User.submission_time <= date_second).all():
        markers.append({
            'icon': 'https://maps.google.com/mapfiles/ms/icons/red-dot.png',
            'lat': user.lat,
            'lng': user.long,
            'name': user.name
        })
    return markers

def get_groups():
    group_codes = []
    for group in User.query.with_entities(User.group_code).distinct().all():
        group_codes.append(group.group_code)
    group_codes = sorted(group_codes)
    return group_codes

def create_csv(group, date_first, date_second):
    date_first = str(parser.parse(date_first).date()).replace(' ', '')
    date_second = str(parser.parse(date_second).date()).replace(' ', '')

    fields = ['Name', 'County', 'Submission Time', 'Email', 'Phone Number', 'Full Address', 'Group Code']
    filename =  f'csv/{group}_{date_first}_{date_second}.csv'
    with open (filename, 'w', newline='\n') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([f'Spreadsheet Generated for Group {group}'])
        csvwriter.writerow(fields)
        voters = []
        for user in User.query.filter_by(group_code=group).filter(User.submission_time >= date_first).filter(User.submission_time <= date_second).order_by(User.submission_time.asc()).all():
            voters.append([
                user.name,
                user.county,
                user.submission_time,
                user.email,
                user.phonenumber,
                user.full_address,
                user.group_code
            ])
        csvwriter.writerows(voters)
    return filename
