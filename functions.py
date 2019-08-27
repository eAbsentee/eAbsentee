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
import json
from typing import Dict
from flask import request, session
from datetime import date
from keys import GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD
import localities_info

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ANNOT_KEY: str = '/Annots'
ANNOT_FIELD_KEY: str = '/T'
ANNOT_VAL_KEY: str = '/V'
ANNOT_RECT_KEY: str = '/Rect'
SUBTYPE_KEY: str = '/Subtype'
WIDGET_SUBTYPE_KEY: str = '/Widget'

input_pdf_path: str = 'static/blankAppFillable.pdf'


def convert_data(data: Dict[str, str]):
    """Rename the keys in the dictionary to match the fields in the PDF. """
    today = date.today()
    todayDate = today.strftime("%m%d%y")
    data_dict = {
        'firstName': data['absentee_first_name'],
        'middleName': data['absentee_middle_name'],
        'lastName': data['absentee_last_name'],
        'suffix': data['absentee_suffix'],
        'ssn': data['absentee_ssn'],
        'reasonCode': data['absentee_reason_code'],
        'registeredToVote': data['election_locality'],
        'supporting': data['absentee_reason_documentation'],
        'birthYear': data['absentee_birth_year'],
        'email': data['absentee_email'],
        'address': data['absentee_street_address'],
        'apt': data['absentee_unit'],
        'city': data['absentee_city'],
        'zipCode': data['absentee_zip'],
        'ballotDeliveryAddress': data['delivery_street_address'],
        'ballotDeliveryCity': data['delivery_city'],
        'ballotDeliveryApt': data['delivery_unit'],
        'ballotDeliveryZip': data['delivery_zip'],
        'ballotDeliveryState': data['delivery_state'],
        'formerFullName': data['absentee_former_name'],
        'formerAddress': data['absentee_former_address'],
        'signature': data['absentee_signature'],
        'firstThreeTelephone': data['absentee_telephone'][0:3],
        'secondThreeTelephone': data['absentee_telephone'][4:7],
        'lastFourTelephone': data['absentee_telephone'][8:12],
        'assistantCheck': 'X' if data['absentee_assistance'] == 'true' else '',
        'assistantFullName': data['assistant_name'],
        'assistantAddress': data['assistant_street_address'],
        'assistantSignature': data['assistant_signature'],
        'assistantApt': data['assistant_unit'],
        'assistantCity': data['assistant_city'],
        'assistantState': data['assistant_state'],
        'assistantZip': data['assistant_zip'],
        'deliverResidence': 'X' if data['delivery_destination'] == 'residence address' else '',
        'deliverMailing': 'X' if data['delivery_destination'] == 'mailing address' else '',
        'deliverEmail': 'X' if data['delivery_destination'] == 'email' else '',
        'genSpecCheck': 'X' if data['election_type'] == 'General or Special Election' else '',
        'demPrimCheck': 'X' if data['election_type'] == 'Democratic Primary' else '',
        'repPrimCheck': 'X' if data['election_type'] == 'Republican Primary' else '',
        'countyCheck': 'X' if 'County' in data['election_locality'] else '',
        'cityCheck': 'X' if 'City' in data['election_locality'] else '',
        'dateMovedMonth': data['absentee_date_moved'][5:7],
        'dateMovedDay': data['absentee_date_moved'][8:10],
        'dateMovedYear': data['absentee_date_moved'][2:4],
        'dateOfElectionMonth': data['election_date'][5:7],
        'dateOfElectionDay': data['election_date'][8:10],
        'dateOfElectionYear': data['election_date'][2:4],
        'todaysDateMonth': todayDate[0:2],
        'todaysDateDay': todayDate[2:4],
        'todaysDateYear': todayDate[4:6]
    }

    # print(data['election_type'])
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)
    return data_dict


def write_fillable_pdf(data: Dict[str, str]):
    data_dict: Dict[str, str] = convert_data(data)
    template_pdf: pdfrw.PdfReader = pdfrw.PdfReader(input_pdf_path)
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(
        NeedAppearances=pdfrw.PdfObject('true')))
    annotations: pdfrw.PdfArray = template_pdf.pages[0][ANNOT_KEY]
    for annotation in annotations:
        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
            if annotation[ANNOT_FIELD_KEY]:
                key = annotation[ANNOT_FIELD_KEY][1:-1]
                if key in data_dict.keys():
                    annotation.update(
                        pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                    )
    pdfrw.PdfWriter().write(session['output_file'], template_pdf)


def parse_data(request: request):
    absentee_first_name: str = request.form['name__first']
    absentee_middle_name: str = request.form['name__middle']
    absentee_last_name: str = request.form['name__last']
    absentee_suffix: str = request.form['name__suffix']
    absentee_ssn: str = request.form['name__ssn']

    election_type: str = request.form['election__type']
    election_date: str = request.form.get('election__date')

    election_locality: str = localities_info.localities[
        request.form['election__locality_gnis']
    ]['locality']

    absentee_reason_code: str = request.form['reason__code']
    absentee_reason_documentation: str = request.form['reason__documentation']

    if request.form.get('more_info__birth_year'):
        absentee_birth_year: str = request.form.get('more_info__birth_year')
    else:
        absentee_birth_year: str = ""

    absentee_telephone: str = request.form.get('more_info__telephone').replace(
        '-', '').replace('(', '').replace(')', '').replace(' ', '')
    absentee_telephone: str = absentee_telephone[:3] + ' ' + \
        absentee_telephone[3:-4] + ' ' + absentee_telephone[-4:]
    absentee_email: str = request.form.get('more_info__email_fax')

    absentee_street_address: str = request.form['address__street']
    absentee_unit: str = request.form['address__unit']
    absentee_city: str = request.form['address__city']
    absentee_state: str = request.form['address__state']
    absentee_zip: str = request.form['address__zip']

    delivery_destination: str = request.form.get('delivery__to')
    delivery_street_address: str = request.form.get('delivery__street')
    delivery_unit: str = request.form.get('delivery__unit')
    delivery_city: str = request.form.get('delivery__city')
    delivery_country: str = request.form.get('country')
    delivery_state: str = request.form.get('deliv-state')
    delivery_zip: str = request.form.get('delivery__zip').replace('-', '')
    # delivery_state_country = request.form.get('delivery__state_or_country')

    absentee_former_name: str = request.form.get('change__former_name')
    absentee_former_address: str = request.form.get('change__former_address')

    if request.form.get('change__date_moved'):
        absentee_date_moved: str = request.form.get('change__date_moved')
    else:
        absentee_date_moved: str = ''

    absentee_assistance: str = request.form.get('assistance__assistance')

    assistant_signed: str = request.form.get('assistant__signed')
    assistant_name: str = request.form.get('assistant__name')
    assistant_street_address: str = request.form.get('assistant__street')
    assistant_unit: str = request.form.get('assistant__unit')
    assistant_city: str = request.form.get('assistant__city')
    assistant_state: str = request.form.get('assistant__state')
    assistant_zip: str = request.form.get('assistant__zip').replace('-', '')
    assistant_signature: str = request.form.get('assistant__sig')

    absentee_agreement: str = request.form['checkbox']  # make it bool instead?

    absentee_signature_date: str = request.form.get('signature__date')

    absentee_signature: str = request.form['signature__signed']

    data: Dict[str, str] = {
        "absentee_first_name": absentee_first_name,
        "absentee_middle_name": absentee_middle_name,
        "absentee_last_name": absentee_last_name,
        "absentee_suffix": absentee_suffix,
        "absentee_ssn": absentee_ssn,
        "election_type": election_type,
        "election_date": election_date,
        "election_locality": election_locality,
        "absentee_reason_code": absentee_reason_code,
        "absentee_reason_documentation": absentee_reason_documentation,
        "absentee_birth_year": absentee_birth_year,
        "absentee_telephone": absentee_telephone,
        "absentee_email": absentee_email,
        "absentee_street_address": absentee_street_address,
        "absentee_unit": absentee_unit,
        "absentee_city": absentee_city,
        "absentee_state": absentee_state,
        "absentee_zip": absentee_zip,
        "delivery_destination": delivery_destination,
        "delivery_street_address": delivery_street_address,
        "delivery_unit": delivery_unit,
        "delivery_city": delivery_city,
        "delivery_country": delivery_country,
        "delivery_state": delivery_state,
        "delivery_zip": delivery_zip,
        "absentee_former_name": absentee_former_name,
        "absentee_former_address": absentee_former_address,
        "absentee_date_moved": absentee_date_moved,
        "absentee_assistance": absentee_assistance,
        "assistant_signed": assistant_signed,
        "assistant_name": assistant_name,
        "assistant_street_address": assistant_street_address,
        "assistant_unit": assistant_unit,
        "assistant_city": assistant_city,
        "assistant_state": assistant_state,
        "assistant_zip": assistant_zip,
        "assistant_signature": assistant_signature,
        "absentee_agreement": absentee_agreement,
        "absentee_signature_date": absentee_signature_date,
        "absentee_signature": absentee_signature
    }
    registrar_address: str = localities_info.localities[request.form[
        'election__locality_gnis']]['email']
    return data, registrar_address


def build_pdf(data: Dict[str, str], registrar_address: str):
    set_session_keys(data, registrar_address)
    write_fillable_pdf(data)
    return registrar_address


def set_session_keys(data: Dict[str, str], registrar_address: str):
    # id is first 10 characters of MD5 hash of dictionary
    id: str = hashlib.md5(repr(data).encode('utf-8')).hexdigest()[:10]
    name: str = data['absentee_first_name'] + \
        ' ' + data['absentee_middle_name'] + \
        ' ' + data['absentee_last_name'] + \
        (', ' + data['absentee_suffix']
         if data['absentee_suffix'].strip() else '')
    session['name'] = name
    session['output_file'] = f'applications/{id}.pdf'
    session['registrar_locality'] = data['election_locality']
    session['registrar_email'] = registrar_address


def email_registrar(registrar_address: str):
    # TODO: keep one server open to minimize SMTP connections
    yagmail.SMTP(GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD).send(
        to='raunakdaga@gmail.com',  # Change when testing, change back when deploying
        # to=registrar_address,
        subject=f'Absentee Ballot Request from {session["name"]}',
        contents='Please find attached an absentee ballot request submitted '
        + f'on behalf of {session["name"]}.',
        attachments=session['output_file'],
        # headers="X-AB-ID"
    )


# def reports(data: Dict[str, str]):
