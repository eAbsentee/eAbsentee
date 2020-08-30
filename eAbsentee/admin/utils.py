import os
import csv
import json
from dateutil import parser
from datetime import datetime
from dotenv import load_dotenv
from eAbsentee.form.models import User

os.chdir(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

def get_users(group, date_first, date_second):
    markers = []
    date_first = parser.parse(date_first)
    date_second = parser.parse(date_second)
    for user in User.query.filter_by(group_code=group).filter(User.submission_time >= date_first).filter(User.submission_time <= date_second).all():
        markers.append({
            'lat': user.lat,
            'lng': user.long,
            'name': user.name,
            'submission_time': user.submission_time
        })
    return markers

def get_groups(current_user):
    if current_user.is_admin():
        group_codes = []
        for group in User.query.with_entities(User.group_code).distinct().all():
            group_codes.append(group.group_code)
        group_codes = sorted(group_codes)
        return group_codes
    else:
        with open('../static/temp_user_groups.json') as file:
            user_groups = json.load(file)
            return sorted(user_groups[current_user.email]["group_codes"])


def create_csv(group, date_first, date_second):
    date_first = str(parser.parse(date_first).date()).replace(' ', '')
    date_second = str(parser.parse(date_second).date()).replace(' ', '')

    group = group.lower()

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
                user.email if user.email else '',
                user.phonenumber if user.phonenumber else '',
                user.full_address,
                user.group_code if user.group_code else ''
            ])
        csvwriter.writerows(voters)
    return filename
