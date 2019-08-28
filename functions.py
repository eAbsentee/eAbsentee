'''
TO-DO VERSION1:
List of written FAQ's
Draft video
Reporting in excel worksheet

DESIGN:
Example websites

In form, general electin prechecked, date 5th of november for all
Move email telephone, birth year below address
Do you want emailed to you? Ask before email
Only pop up email/fax if 6A-6D selected on reason
May gray out different mailing address and email/fax and change name/address
Telephone - why registrar has questions
/s automatically applied - check if is required
Designing help
5 digit zip code only

Person who's canvassing
Administrative optional info collection below signature - what district the race is
house senate statewide

colect which canvasser/district they're in | race of interest | after submitted
on confirmation page | 3 letter initial code

add mr surovell, mr rouvelas onto report emails
change mail address to please mail to another address
ip address for report https://stackoverflow.com/questions/3759981/get-ip-address-of-visitors-using-flask-for-python

on form page have an option to print out and send but comment it out because we may need for future

TO-DO VERSION2:
Turn off ability to submit
'''

import hashlib
import yagmail
import pdfrw
import os
import xlwt
from typing import Dict
from flask import request, session
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


''' First, data is parsed from the form. @sumanth, i combined the two data parsing and converting functions'''


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
        'application_ip': request.remote_addr
    }

    registrar_address: str = localities_info.localities[request.form[
        'election__locality_gnis']]['email']
    return data_dict, registrar_address


def build_pdf(data: Dict[str, str], registrar_address: str):
    set_session_keys(data, registrar_address)
    write_fillable_pdf(data)
    return registrar_address


def set_session_keys(data: Dict[str, str], registrar_address: str):
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


''' A report is written daily at {} to be sent to Mr. Surovell, and Mr. rouvelas
Later, update to send report to anyone'''


def write_report(filename, sheet, list1, list2, x, y, z):
    book = xlwt.Workbook()
    # sh = book.add_sheet(sheet)
    #
    # variables = [x, y, z]
    # x_desc = 'Display'
    # y_desc = 'Dominance'
    # z_desc = 'Test'
    # desc = [x_desc, y_desc, z_desc]
    #
    # col1_name = 'Stimulus Time'
    # col2_name = 'Reaction Time'
    #
    # # You may need to group the variables together
    # # for n, (v_desc, v) in enumerate(zip(desc, variables)):
    # for n, v_desc, v in enumerate(zip(desc, variables)):
    #     sh.write(n, 0, v_desc)
    #     sh.write(n, 1, v)
    #
    # n += 1
    #
    # sh.write(n, 0, col1_name)
    # sh.write(n, 1, col2_name)
    #
    # for m, e1 in enumerate(list1, n+1):
    #     sh.write(m, 0, e1)
    #
    # for m, e2 in enumerate(list2, n+1):
    #     sh.write(m, 1, e2)
    #
    book.save(filename)
