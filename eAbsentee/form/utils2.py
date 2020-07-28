import hashlib
import yagmail
import os, sys
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

# Change current working directory to directory 'functions.py' is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()


def application_process(request, group_code_form=None):
    data = parse_data(request, group_code_form=group_code_form)
    write_pdf(data, request)
    add_to_database(data, request)
    email_registrar(data)
    os.remove(data['output_file'])

def parse_data(request, group_code_form):
    data = {}

    group_code = ''
    if group_code_form:
        group_code = group_code_form.lower()
    elif request.cookies.get('group'):
        group_code = request.cookies.get('group').lower()

    emails_to_send = []
    with open('../static/localities_info.json') as file:
        localities = json.load(file)
        if os.environ["FLASK_DEBUG"] == True:
            emails_to_send = ['applications@eabsentee.org']
        else:
            emails_to_send = [localities[request.form['registered_county']]['email']]

        if request.form.get('email'):
            emails_to_send.append(request.form.get('email'))

    with open('../static/localities_info.json') as file:
        localities = json.load(file)
        data = {
            'full_name': (request.form['name_first'] + ' ' + request.form['name_middle'] + ' ' + request.form['name_last']).replace('  ', ' '),
            'full_address': request.form['address'] + ((' ' + request.form['apt']) if request.form['apt'] else '') + ', ' + request.form['city'] + ', ' + 'VA' +  ' ' + request.form['zip'],
            'phonenumber': request.form.get('phonenumber').replace(
                '-', '').replace('(', '').replace(')', '').replace(' ', '').replace('+1', '').replace('-', '').replace('.', '').replace('+', ''),
            'group_code': group_code,
            'emails_to_send': emails_to_send
        }

    data['application_id'] = hashlib.md5(repr(data).encode('utf-8')).hexdigest()[: 24]
    data['output_file'] = data['application_id'] + '.pdf'

    return data

def write_pdf(data, request):
    today_date = date.today().strftime('%m%d%y')

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(180, 732, request.form['name_last'])
    can.drawString(410, 732, request.form['name_first'])
    can.drawString(190, 715, request.form['name_middle'])
    can.drawString(405, 715, request.form['suffix'])

    can.drawString(525, 698, '  '.join(request.form['ssn'])) # SSN
    can.drawString(282, 683, 'X') # Gen/Spec
    # can.drawString(405, 683, 'X') # Dem Prim
    # can.drawString(503, 683, 'X') # Republican Primary
    can.drawString(212, 670, '11') # Month of Election
    can.drawString(261, 670, '03') # Day of Election
    can.drawString(310, 670, '20') # Year of Election
    can.drawString(428, 670, request.form['registered_county']) # City/County
    # can.drawString(409, 658, 'X') # Vote by Mail in All Elections Yes
    # can.drawString(442, 658, 'X') # Vote by Mail in All Elections No
    # can.drawString(126, 633, 'X') # Dem Primary Ballots
    # can.drawString(234, 633, 'X') # Rep Primary Ballots
    # can.drawString(331, 633, 'X') # No Primary Ballots

    can.drawString(165, 614, request.form['address'])
    can.drawString(535, 614, request.form['apt'])
    can.drawString(145, 596, request.form['city'])
    can.drawString(408, 596, '   '.join(request.form['zip']))

    can.drawString(198, 480, request.form['former_name'])
    can.drawString(198, 464, request.form['former_address'])
    # can.drawString(158, 448, 'City')
    # can.drawString(398, 448, 'State')
    # can.drawString(477, 448, '     '.join('20171'))
    can.drawString(525, 464, request.form['date_moved'])


    can.drawString(128, 301, 'X' if request.form.get(
        'assistance_check') == 'true' else '',)
    can.drawString(210, 258, request.form['assistant_name'])
    # can.drawString(510, 258, 'Asssitant Phone')
    can.drawString(210, 240, request.form['assistant_address']))
    can.drawString(560, 240, request.form['assistant_apt'])
    can.drawString(150, 226, request.form['assistant_city'])
    can.drawString(385, 226, request.form['assistant_state'])
    can.drawString(482, 226, '     '.join(request.form['assistant_zip']))
    can.drawString(210, 176, request.form['assistant_name'])
    can.drawString(460, 176, today_date)

    can.drawString(165, 565, request.form['different_address'])
    can.drawString(545, 565, request.form['different_apt'])
    can.drawString(145, 548, request.form['different_city'])
    can.drawString(322, 548, request.form['different_state'])
    can.drawString(418, 548, '   '.join(request.form['different_zip']))
    can.drawString(558, 548, request.form['different_country'] if request.form['different_city'] else '')

    can.drawString(175, 509, request.form['email'])
    can.drawString(275, 115, '/s/ ' + request.form['signature'].strip())
    can.drawString(485, 115, today_date[0:2])
    can.drawString(525, 115, today_date[2:4])
    can.drawString(565, 115, today_date[4:6])

    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    existing_pdf = PdfFileReader('../static/pdf/form.pdf', 'rb')
    output = PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    with open(data['output_file'], 'wb') as output_pdf_file:
        output.write(output_pdf_file)

def add_to_database(data, request):
    new_voter = User(
        application_id=data['application_id'],
        name=data['full_name'],
        county=request.form['registered_county'],
        email=request.form['email'],
        phonenumber=data['phonenumber'],
        full_address=data['full_address'],
        ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
        group_code=data['group_code'],
        lat=request.form['lat'],
        long=request.form['long']
    )

    db.session.add(new_voter)
    db.session.commit()


def email_registrar(data):
    """Email the form to the registrar of the applicant's locality. """
    yagmail.SMTP(os.environ["GMAIL_SENDER_ADDRESS"], os.environ["GMAIL_SENDER_PASSWORD"]).send(
        to=([email for email in data['emails_to_send']]),
        subject=('Absentee Ballot Request - Applicant-ID: ' +
        f'{data["application_id"]}'),
        contents='Please find attached an absentee ballot request ' +
        f'submitted on behalf of {data["full_name"]} from eAbsentee.org',
        attachments=data['output_file']
    )