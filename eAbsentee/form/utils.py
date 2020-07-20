import hashlib
import yagmail
import os
import json
import datetime
import io
import csv
from flask import request
from datetime import date
from datetime import datetime
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from dotenv import load_dotenv
from .models import db, User
from sqlalchemy.exc import IntegrityError

# Change current working directory to directory 'functions.py' is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()


def application_process(request, group_code_form=None):
    data = parse_data(request, group_code_form=group_code_form)
    write_pdf(data)
    add_to_database(data)
    email_registrar(data)
    os.remove(data['application_id'] + '.pdf')

def parse_data(request, group_code_form):
    data = {}
    today_date = date.today().strftime('%m%d%y')

    group_code = ''
    if group_code_form:
        group_code = lower(group_code_form)
    elif request.cookies.get('group'):
        group_code = lower(request.cookies.get('group'))

    emails_to_be_sent_to = []
    with open('../static/localities_info.json') as file:
        localities = json.load(file)

        if os.environ["TESTING_MODE"] == True:
            emails_to_be_sent_to = ['applications@eabsentee.org']
        else:
            emails_to_be_sent_to = [localities[request.form['registered_county']]['email']]


        if request.form.get('email'):
            emails_to_be_sent_to.append(request.form.get('email'))

    phonenumber = request.form.get('phonenumber').replace(
        '-', '').replace('(', '').replace(')', '').replace(' ', '').replace('+1', '').replace('-', '').replace('.', '').replace('+', '')

    with open('../static/localities_info.json') as file:
        localities = json.load(file)
        data = {
            'first_name': request.form['name_first'],
            'middle_name': request.form['name_middle'],
            'last_name': request.form['name_last'],
            'suffix': request.form['name_suffix'],
            'full_name': request.form['name_first'] + ' ' + request.form['name_middle'] + ' ' + request.form['name_last'],
            'ssn': '  '.join(request.form['ssn']),
            'registered_to_vote': request.form['registered_county'],
            'email': request.form['email'],
            'address': request.form['address'],
            'apt': request.form['apt'],
            'city': request.form['city'],
            'zip_code': '   '.join(request.form['zip']),
            'state': 'VA',
            'full_address': request.form['address'] + ((' ' + request.form['apt']) if request.form['apt'] else '') + ', ' + request.form['city'] + ', ' + 'VA' +  ' ' + request.form['zip'],
            'full_delivery_address': request.form['different_address'] +      ((' ' + request.form['different_apt']) if request.form['different_apt'] else ' ') + ', ' + request.form['different_city'] + ', ' + request.form['different_state'] +  ' ' + request.form['different_zip'] + ' ' + request.form['different_country'],
            'delivery_address': request.form.get('different_address'),
            'delivery_city': request.form.get('different_city'),
            'delivery_apt': request.form.get('different_apt'),
            'delivery_zip': '   '.join(request.form.get( 'different_zip').replace('-', '')),
            'delivery_country': request.form['different_country'] if request.form['different_city'] else '',
            'delivery_state': request.form.get('different_state'),
            'signature': '/S/ ' + request.form[
                'signature'].replace('/S/', '', 1).strip(),
            'phonenumber': phonenumber,
            'assistant_check': 'X' if request.form.get(
                'assistance_check') == 'true' else '',
            'assistant_fullname': request.form.get('assistant_name'),
            'assistant_address': request.form.get('assistant_address'),
            'assistant_signature': request.form.get('assistant_name'),
            'assistant_apt': request.form.get('assistant_apt'),
            'assistant_city': request.form.get('assistant_city'),
            'assistant_state': request.form.get('assistant_state'),
            'assistant_zip': '   '.join(request.form.get(
                'assistant_zip').replace('-', '')),
            'deliver_residence': 'X' if request.form.get(
                'different_address_check') == 'false' else '',
            'deliver_mailing': 'X' if request.form.get(
                'different_address_check') == 'true' else '',
            'county_check': 'X' if 'County' in localities[
                request.form['registered_county']]['locality'] else '',
            'city_check': 'X' if 'City' in localities[
                request.form['registered_county']]['locality'] else '',
            'date_today_month': today_date[0:2],
            'date_today_day': today_date[2:4],
            'date_today_year': today_date[4:6],
            'application_ip': request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
            'group_code': group_code,
            'emails_to_be_sent_to': emails_to_be_sent_to
        }

    data['application_id'] = hashlib.md5(repr(data).encode('utf-8')).hexdigest()[: 24]
    data['output_file'] = data['application_id'] + '.pdf'

    return data

def write_pdf(data):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(180, 732, data['last_name'])
    can.drawString(410, 732, data['first_name'])
    can.drawString(190, 715, data['middle_name'])
    can.drawString(405, 715, data['suffix'])

    can.drawString(525, 698, (data['ssn'])) # SSN
    can.drawString(282, 683, 'X') # Gen/Spec
    # can.drawString(405, 683, 'X') # Dem Prim
    # can.drawString(503, 683, 'X') # Republican Primary
    can.drawString(212, 670, '11') # Month of Election
    can.drawString(261, 670, '03') # Day of Election
    can.drawString(310, 670, '20') # Year of Election
    can.drawString(428, 670, data['registered_to_vote']) # City/County of
    # can.drawString(409, 658, 'X') # Vote by Mail in All Elections Yes
    # can.drawString(442, 658, 'X') # Vote by Mail in All Elections No
    # can.drawString(126, 633, 'X') # Dem Primary Ballots
    # can.drawString(234, 633, 'X') # Rep Primary Ballots
    # can.drawString(331, 633, 'X') # No Primary Ballots

    can.drawString(165, 614, data['address'])
    can.drawString(535, 614, data['apt'])
    can.drawString(145, 596, data['city'])
    can.drawString(408, 596, ''.join(data['zip_code']))

    can.drawString(165, 565, data['delivery_address'])
    can.drawString(545, 565, data['delivery_apt'])
    can.drawString(145, 548, data['delivery_city'])
    can.drawString(322, 548, data['delivery_state'])
    can.drawString(418, 548, ''.join(data['delivery_zip']))
    can.drawString(558, 548, data['delivery_country'])

    can.drawString(175, 509, data['email'])
    can.drawString(275, 115, data['signature'])
    can.drawString(485, 115, data['date_today_month'])
    can.drawString(525, 115, data['date_today_day'])
    can.drawString(565, 115, data['date_today_year'])

    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    existing_pdf = PdfFileReader('../static/pdf/form.pdf', 'rb')
    output = PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    output.write(open(data['output_file'], 'wb'))

def add_to_database(data):
    new_voter = User(
        application_id=data['application_id'],
        name=data['full_name'],
        county=data['registered_to_vote'],
        email=data['email'],
        phonenumber=data['phonenumber'],
        full_address=data['full_address'],
        ip=data['application_ip'],
        group_code=data['group_code']
    )

    db.session.add(new_voter)
    db.session.commit()

def email_registrar(data):
    """Email the form to the registrar of the applicant's locality. """
    yagmail.SMTP(os.environ["GMAIL_SENDER_ADDRESS"], os.environ["GMAIL_SENDER_PASSWORD"]).send(
        to=([email for email in data['emails_to_be_sent_to']]),
        subject=('Absentee Ballot Request - Applicant-ID: ' +
        f'{data["application_id"]}'),
        contents='Please find attached an absentee ballot request ' +
        f'submitted on behalf of {data["full_name"]} from eAbsentee.org',
        attachments=data['output_file']
    )


def add_to_database_all_voters():
    filename = '../static/voters.csv'

    with open(filename, 'r', encoding='cp1252') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)

        for row in csvreader:
            from dateutil import parser
            # datetime_object = datetime.strptime(row[1], '%m/%d/%Y %H:%S')
            # print(type(parser.parse(row[1])))
            # print(row)
            new_voter = User(
                application_id=row[7],
                name=row[0],
                submission_time=parser.parse(row[1]),
                county=row[2],
                email=row[3],
                phonenumber=row[4],
                full_address=row[5],
                ip=row[6],
                group_code=row[7]
            )
            try:
                db.session.add(new_voter)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print("Duplicate entry detected!")
