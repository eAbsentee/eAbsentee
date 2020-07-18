import yagmail
import os
import json
from openpyxl import load_workbook
from flask import request
from dotenv import load_dotenv

# Change current working directory to directory 'functions.py' is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

GMAIL_SENDER_ADDRESS = os.environ["GMAIL_SENDER_ADDRESS"]
GMAIL_SENDER_PASSWORD = os.environ["GMAIL_SENDER_PASSWORD"]
API_KEY = os.environ["GMAIL_SENDER_PASSWORD"]
API_KEY_FCDC = os.environ["API_KEY_FCDC"]


def add_to_groups(request):
    if request.form.get('api_key') != API_KEY:
        return
    if request.form.get('group_code'):
        with open('static/groups.json') as file:
            groups = json.load(file)

            new_group = {
                request.form.get('group_code'): {
                    'email': request.form.get('group_email')
                    }
            }

            groups.update(new_group)
            with open('static/groups.json', 'w') as f:
                json.dump(groups, f, indent=4, sort_keys=True)

def add_group_fcdc(request):
    if request.form.get('api_key') != API_KEY_FCDC:
        return

    if request.form.get('keycode'):
        with open('static/groups.json') as file:
            groups = json.load(file)
            new_group = {
                request.form.get('keycode'): {
                    "email": request.form.get('group_email')
                }
            }
            groups.update(new_group)
            with open('static/groups.json', 'w') as f:
                json.dump(groups, f, indent=4, sort_keys=True)


def email_report_alltime_api(request):
    report_path = f'reports/all_time.xlsx'
    report = load_workbook(filename=report_path)
    worksheet = report.active
    if request.form.get('api_key') == API_KEY:
        if worksheet['A2'].value:
            yagmail.SMTP(GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD).send(
                to=request.form.get('email_spreadsheet'),
                subject=f'Absentee Ballot Application Report',
                attachments=f'reports/all_time.xlsx'
            )
