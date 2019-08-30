"""
TO-DO VERSION1:

Move from keys.py to environemnt variables when deploying
Change confirmation page to index style
Only pop up email/fax if 6A-6D selected on reason
/s automatically applied - check if is required

TO-DO VERSION2:
Turn off ability to submit
Person who's canvassing
Administrative optional info collection below signature - what district the race is
house senate statewide
"""

import hashlib
import yagmail
import pdfrw
import os
import json
import openpyxl
from openpyxl import load_workbook
from typing import Dict, List, Tuple
from flask import request, session
import datetime
from datetime import date
from keys import GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD
import localities_info

# Change current working directory (needed for Atom development)
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


def parse_data(request: request) -> Tuple[Dict[str, str], str]:
    """ Parse data from the form and convert into a dict format
    to allow it to be passed to the PDF filler. """

    todayDate: str = date.today().strftime("%m%d%y")

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
        'ballotDeliveryZip': request.form.get(
            'delivery__zip').replace('-', ''),
        'ballotDeliveryState': request.form.get('deliv-state'),
        'formerFullName': request.form.get('change__former_name'),
        'formerAddress': request.form.get('change__former_address'),
        'signature': '/S/ ' + request.form[
            'signature__signed'].replace('/S/', '', 1).strip(),
        'firstThreeTelephone': absentee_telephone[0:3],
        'secondThreeTelephone': absentee_telephone[3:6],
        'lastFourTelephone': absentee_telephone[6:10],
        'assistantCheck': 'X' if request.form.get(
            'assistance__assistance') == 'true' else '',
        'assistantFullName': request.form.get('assistant__name'),
        'assistantAddress': request.form.get('assistant__street'),
        'assistantSignature': request.form.get('assistant__sig'),
        'assistantApt': request.form.get('assistant__unit'),
        'assistantCity': request.form.get('assistant__city'),
        'assistantState': request.form.get('assistant__state'),
        'assistantZip': request.form.get('assistant__zip').replace('-', ''),
        'deliverResidence': 'X' if request.form.get(
            'delivery__to') == 'residence address' else '',
        'deliverMailing': 'X' if request.form.get(
            'delivery__to') == 'mailing address' else '',
        'deliverEmail': 'X' if request.form.get(
            'delivery__to') == 'email' else '',
        'genSpecCheck': 'X' if request.form[
            'election__type'] == 'General or Special Election' else '',
        'demPrimCheck': 'X' if request.form[
            'election__type'] == 'Democratic Primary' else '',
        'repPrimCheck': 'X' if request.form[
            'election__type'] == 'Republican Primary' else '',
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


def build_pdf(data: Dict[str, str], registrar_address: str) -> str:
    """Takes in an input of the data dictionary,
    along with the email address of the respective registrar.
    It calls set_session_keys, and then write_fillable_pdf,
    and then appends the data to the report, and then
    sends the registrar address to email_registrar."""

    set_session_keys(data, registrar_address)
    write_fillable_pdf(data)

    today_date: str = date.today().strftime("%m-%d-%y")
    report_path: str = f'reports/{today_date}.xlsx'

    data_for_report: List[str] = [
        session['name'],
        str(datetime.datetime.now().time()),
        data['ssn'],
        data['reasonCode'],
        data['supporting'],
        data['registeredToVote'],
        data['email'],
        data['firstThreeTelephone']
        + data['secondThreeTelephone'] + data['lastFourTelephone'],
        data['address'] + data['apt'] + ', '
        + data['city'] + ', ' + data['zipCode'],
        data['applicationIP'],
        session['application_id'],
        data['canvasserId']
    ]

    append_to_report(report_path, data_for_report)
    return registrar_address


def set_session_keys(data: Dict[str, str], registrar_address: str) -> None:
    # id is first 10 characters of MD5 hash of dictionary
    id: str = hashlib.md5(repr(data).encode('utf-8')).hexdigest()[:10]
    name: str = data['firstName'] + \
        ' ' + data['middleName'] + \
        ' ' + data['lastName'] + \
        (', ' + data['suffix']
         if data['suffix'].strip() else '')
    session['name'] = name
    session['application_id'] = id
    session['output_file'] = f'applications/{id}.pdf'
    session['registrar_locality'] = data['registeredToVote']
    session['registrar_email'] = registrar_address

    today_date: str = date.today().strftime("%m-%d-%y")
    session['report_file'] = f'reports/{today_date}.xlsx'


def write_fillable_pdf(data: Dict[str, str]) -> None:
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


def email_registrar(registrar_address: str) -> None:
    # TODO: keep one server open to minimize SMTP connections
    yagmail.SMTP(GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD).send(
        to='raunakdaga@gmail.com',
        # to=registrar_address,
        subject=f'Absentee Ballot Request from {session["name"]}',
        contents='Please find attached an absentee ballot request ' + \
        f'submitted on behalf of {session["name"]}.',
        attachments=session['output_file']
    )


def create_report() -> None:
    """ Call this daily at 5 am somehow, then save the filename for the day.
    It is not needed to save because it is just {thedate}.xls basically. """

    today_date: str = date.today().strftime("%m-%d-%y")

    report: openpyxl.workbook.Workbook = openpyxl.Workbook()
    sh: openpyxl.worksheet.worksheet.Worksheet = report.active
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
    sh['K1'] = 'Form ID'
    sh['L1'] = 'Canvasser ID'
    report_path: str = f'reports/{today_date}.xlsx'

    report.save(report_path)
    return report_path


def append_to_report(report_path: str, data: Dict[str, str]) -> None:
    if not os.path.isfile(report_path):
        create_report()
    report: openpyxl.workbook.Workbook = load_workbook(filename=report_path)
    worksheet: openpyxl.worksheet.worksheet.Worksheet = report.active
    worksheet.append(data)
    report.save(report_path)


def email_report() -> None:
    today_date: str = date.today().strftime("%m-%d-%y")
    yagmail.SMTP(GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD).send(
        to=['raunakdaga@gmail.com'],
        # to=['ssurovell@gmail.com', 'lerouvelas@gmail.com']
        subject=f'Daily Absentee Ballot Application Report - {today_date}',
        contents=f'Please find attached the daily report of absentee ' + \
        f'ballot applications for {today_date}.',
        attachments=f'reports/{today_date}.xlsx'
    )
