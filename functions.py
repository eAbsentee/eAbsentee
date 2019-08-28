'''
TO-DO VERSION1:
Draft video

Move from keys.py to environemnt variables when deploying

Do you want emailed to you? Ask before email
Only pop up email/fax if 6A-6D selected on reason
May gray out different mailing address and email/fax and change name/address
/s automatically applied - check if is required
5 digit zip code only

TO-DO VERSION2:
Turn off ability to submit

Person who's canvassing
Administrative optional info collection below signature - what district the race is
house senate statewide
'''

import hashlib
import yagmail
import pdfrw
import os
import openpyxl
from openpyxl import load_workbook
from typing import Dict
from flask import request, session
import datetime
from datetime import date
from keys import GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD
import localities_info

# Change current working directory (needed for Atom development; I wish I knew how to make Atom work)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Subtypes of pdfrw
ANNOT_KEY: str = '/Annots'
ANNOT_FIELD_KEY: str = '/T'
ANNOT_VAL_KEY: str = '/V'
ANNOT_RECT_KEY: str = '/Rect'
SUBTYPE_KEY: str = '/Subtype'
WIDGET_SUBTYPE_KEY: str = '/Widget'

# Where the fillable form lives
input_pdf_path: str = 'static/blankAppFillable.pdf'


''' First, data is parsed from the form, and converted into a dict format
to allow it to be passed to the pdf filler. '''


def parse_data(request: request):
    today = date.today()
    todayDate = today.strftime("%m%d%y")

    absentee_telephone: str = request.form.get('more_info__telephone').replace(
        '-', '').replace('(', '').replace(')', '').replace(' ', '')

    data_dict: Dict[str, str] = {
        'firstName': request.form['name__first'],
        'middleName': request.form['name__middle'],
        'lastName': request.form['name__last'],
        'suffix': request.form['name__suffix'],
        'ssn': request.form['name__ssn'],
        'reasonCode': request.form['reason__code'],
        'registeredToVote': localities_info.localities[
            request.form['election__locality_gnis']
        ]['locality'],
        'supporting': request.form['reason__documentation'],
        'birthYear': request.form.get('more_info__birth_year'),
        'email': request.form.get('more_info__email_fax'),
        'address': request.form['address__street'],
        'apt': request.form['address__unit'],
        'city': request.form['address__city'],
        'zipCode': request.form['address__zip'],
        'ballotDeliveryAddress': request.form.get('delivery__street'),
        'ballotDeliveryCity': request.form.get('delivery__city'),
        'ballotDeliveryApt': request.form.get('delivery__unit'),
        'ballotDeliveryZip': request.form.get('delivery__zip').replace('-', ''),
        'ballotDeliveryState': request.form.get('deliv-state'),
        'formerFullName': request.form.get('change__former_name'),
        'formerAddress': request.form.get('change__former_address'),
        'signature': request.form['signature__signed'],
        'firstThreeTelephone': absentee_telephone[0:3],
        'secondThreeTelephone': absentee_telephone[3:6],
        'lastFourTelephone': absentee_telephone[6:10],
        'assistantCheck': 'X' if request.form.get('assistance__assistance') == 'true' else '',
        'assistantFullName': request.form.get('assistant__name'),
        'assistantAddress': request.form.get('assistant__street'),
        'assistantSignature': request.form.get('assistant__sig'),
        'assistantApt': request.form.get('assistant__unit'),
        'assistantCity': request.form.get('assistant__city'),
        'assistantState': request.form.get('assistant__state'),
        'assistantZip': request.form.get('assistant__zip').replace('-', ''),
        'deliverResidence': 'X' if request.form.get('delivery__to') == 'residence address' else '',
        'deliverMailing': 'X' if request.form.get('delivery__to') == 'mailing address' else '',
        'deliverEmail': 'X' if request.form.get('delivery__to') == 'email' else '',
        'genSpecCheck': 'X' if request.form['election__type'] == 'General or Special Election' else '',
        'demPrimCheck': 'X' if request.form['election__type'] == 'Democratic Primary' else '',
        'repPrimCheck': 'X' if request.form['election__type'] == 'Republican Primary' else '',
        'countyCheck': 'X' if 'County' in localities_info.localities[
            request.form['election__locality_gnis']
        ]['locality'] else '',
        'cityCheck': 'X' if 'City' in localities_info.localities[
            request.form['election__locality_gnis']
        ]['locality'] else '',
        'dateMovedMonth': request.form.get('change__date_moved')[5:7],
        'dateMovedDay': request.form.get('change__date_moved')[8:10],
        'dateMovedYear': request.form.get('change__date_moved')[2:4],
        'dateOfElectionMonth': request.form.get('election__date')[5:7],
        'dateOfElectionDay': request.form.get('election__date')[8:10],
        'dateOfElectionYear': request.form.get('election__date')[2:4],
        'todaysDateMonth': todayDate[0:2],
        'todaysDateDay': todayDate[2:4],
        'todaysDateYear': todayDate[4:6],
        'canvasserId': request.form.get('canvasser_id'),
        'applicationIP': request.remote_addr
    }

    registrar_address: str = localities_info.localities[request.form[
        'election__locality_gnis']]['email']
    return data_dict, registrar_address


''' build_pdf() takes in an input of the data dictionary,
along with the email address of the respective registrar.
it calls set_session_keys, and then write_fillable_pdf,
and then appends the data to the report, and then
sends the registrar address to email_registrar'''


def build_pdf(data: Dict[str, str], registrar_address: str):
    today = date.today()
    set_session_keys(data, registrar_address, today)
    write_fillable_pdf(data)

    today_date = today.strftime("%m-%d-%y")
    report_path = 'reports/' + today_date + '.xlsx'

    data_for_report = [
        session['name'],
        str(datetime.datetime.now().time()),
        data['ssn'],
        data['reasonCode'],
        data['supporting'],
        data['registeredToVote'],
        data['email'],
        data['firstThreeTelephone'] + data['secondThreeTelephone'] + data['lastFourTelephone'],
        data['address'] + data['apt'] + ', ' + data['city'] + ', ' + data['zipCode'],
        data['applicationIP'],
        data['canvasserId']
    ]

    append_to_report(report_path, data_for_report)
    return registrar_address


def set_session_keys(data: Dict[str, str], registrar_address: str, today):
    # id is first 10 characters of MD5 hash of dictionary
    id: str = hashlib.md5(repr(data).encode('utf-8')).hexdigest()[:10]
    name: str = data['firstName'] + \
        ' ' + data['middleName'] + \
        ' ' + data['lastName'] + \
        (', ' + data['suffix']
         if data['suffix'].strip() else '')
    session['name'] = name
    session['output_file'] = f'applications/{id}.pdf'
    session['registrar_locality'] = data['registeredToVote']
    session['registrar_email'] = registrar_address

    today_date = today.strftime("%m-%d-%y")
    session['report_file'] = 'reports/' + today_date + '.xlsx'


def write_fillable_pdf(data: Dict[str, str]):
    template_pdf: pdfrw.PdfReader = pdfrw.PdfReader(input_pdf_path)
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(
        NeedAppearances=pdfrw.PdfObject('true')))
    annotations: pdfrw.PdfArray = template_pdf.pages[0][ANNOT_KEY]
    for annotation in annotations:
        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
            if annotation[ANNOT_FIELD_KEY]:
                key = annotation[ANNOT_FIELD_KEY][1:-1]
                if key in data.keys():
                    annotation.update(
                        pdfrw.PdfDict(V='{}'.format(data[key]))
                    )
    pdfrw.PdfWriter().write(session['output_file'], template_pdf)


'''Emailing the registrar is the very last thing to be done in the workflow.'''


def email_registrar(registrar_address: str):
    # TODO: keep one server open to minimize SMTP connections
    yagmail.SMTP(GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD).send(
        to='raunakdaga@gmail.com',  # Change when testing, change back when deploying
        # to=registrar_address,
        subject=f'Absentee Ballot Request from {session["name"]}',
        contents='Please find attached an absentee ballot request submitted ' + \
        f'on behalf of {session["name"]}.',
        attachments=session['output_file'],
        # headers="X-AB-ID"
    )


''' Call this daily at 5 am somehow, then save the filename for the day.
It is honestly not needed to save because it is just {thedate}.xls basically.'''


def create_report():
    today = date.today()
    today_date = today.strftime("%m-%d-%y")

    report = openpyxl.Workbook()
    sh = report.active
    sh['A1'] = 'Applicant Name'
    sh['B1'] = 'Time Submitted'
    sh['C1'] = 'SSN'
    sh['D1'] = 'Reason Code'
    sh['E1'] = 'Supporting Information'
    sh['F1'] = 'Registered to Vote Where'
    sh['G1'] = 'Email'
    sh['H1'] = 'Telephone Number'
    sh['I1'] = 'Address'
    sh['J1'] = 'IP Submitted From'
    sh['K1'] = 'Canvasser ID'
    report_path = 'reports/' + today_date + '.xlsx'

    report.save(report_path)
    return report_path


def append_to_report(report_path, data):
    report = load_workbook(report_path)
    worksheet = report.active
    worksheet.append(data)
    report.save(report_path)


def email_report():
    today = date.today()
    today_date = today.strftime("%m-%d-%y")
    yagmail.SMTP(GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD).send(
        to=['raunakdaga@gmail.com'],  # Add mr surovell, mr rouvelas onto report emails
        subject=f'Daily Absentee Ballot Application Report - {today_date} ',
        contents='Please find attached the daily report of absentee ballot applications.',
        attachments='reports/{today_date}.xlsx'
    )
