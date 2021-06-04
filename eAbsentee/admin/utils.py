import os
import csv
import yagmail
from dateutil import parser
from datetime import datetime
from dotenv import load_dotenv
from eAbsentee.form.models import User
from eAbsentee.admin.models import GroupReference

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
    group_codes = []
    if current_user.is_admin():
        for group in User.query.with_entities(User.group_code).distinct().all():
            group_codes.append(group.group_code)
    else:
        for group_reference in GroupReference.query.filter_by(email=current_user.email).all():
            group_codes.append(group_reference.group_code)
    group_codes = sorted(group_codes)
    return group_codes

def create_csv(group, date_first, date_second, current_user):
    date_first = str(parser.parse(date_first).date()).replace(' ', '')
    date_second = str(parser.parse(date_second).date()).replace(' ', '')

    # TODO: Standardize lower-casing of groups... tsktsk too much technical debt
    group = group.lower()

    fields = ['Name', 'County', 'Submission Time', 'Email', 'Phone Number', 'Full Address', 'Group Code', 'Election Date']
    filename =  f'csv/{group}_{date_first}_{date_second}.csv'
    with open (filename, 'w', newline='\n') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([f'Spreadsheet Generated for User {current_user.email}'])
        csvwriter.writerow(fields)

        possible_users = User.query if current_user.is_admin() and group == 'all_voters' else User.query.filter_by(group_code=group)
        possible_users = possible_users.filter(User.submission_time >= date_first, User.submission_time <= date_second).order_by(User.submission_time.asc())

        voters = []
        for user in possible_users:
            voters.append([
                user.name,
                user.county,
                user.submission_time,
                user.email if user.email else '',
                user.phonenumber if user.phonenumber else '',
                user.full_address,
                user.group_code if user.group_code else '',
                user.election_date,
            ])

        csvwriter.writerows(voters)
    return filename

def email_reminder(email):
    yagmail.SMTP(os.environ['GMAIL_SENDER_ADDRESS'], os.environ['GMAIL_SENDER_PASSWORD']).send(
        to=email,
        subject=f'Reminder to check eAbsentee data portal',
        contents=f'New absentee ballot applications were submitted ' +
        'recently using your eAbsentee.org group codes. ' +
        'Please email raunak@eAbsentee.org with any questions.'
    )
