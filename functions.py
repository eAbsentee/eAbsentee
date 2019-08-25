from typing import Dict
from datetime import datetime
from flask import request
import hashlib
import yagmail
from keys import GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD
import localitiesAndReasons
from buildPDF import write_fillable_pdf


def parse_data(request: request):
    absentee_first_name: str = request.form['name__first']
    absentee_middle_name: str = request.form['name__middle']
    absentee_last_name: str = request.form['name__last']
    absentee_suffix: str = request.form['name__suffix']
    absentee_ssn: str = request.form['name__ssn']

    election_type: str = request.form['election__type']
    election_date: str = datetime.strftime(datetime.strptime(
        request.form['election__date'], '%d-%m-%y'), '%m %d %y')
    election_locality: str = localitiesAndReasons.localities[request.form['election__locality_gnis']]['locality']

    absentee_reason: str = localitiesAndReasons.reasons[request.form['reason__code']]
    absentee_reason_documentation: str = request.form['reason__documentation']

    absentee_birth_year: str = datetime.strftime(datetime.strptime(
        request.form.get('more_info__birth_year'), '%y'), '%y')
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
    # delivery_state_country: str = request.form.get('delivery__state_or_country')

    absentee_former_name: str = request.form.get('change__former_name')
    absentee_former_address: str = request.form.get('change__former_address')
    absentee_date_moved: str = (datetime.strftime(datetime.strptime(request.form.get(
        'change__date_moved'), '%d-%m-%y'), '%m %d %y')
        if request.form.get('change__date_moved') else "")
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
    absentee_signature_date: str = datetime.strftime(datetime.strptime(
        request.form['signature__date'], '%d-%m-%y'), '%m %d %y')
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
        "absentee_reason": absentee_reason,
        "absentee_reason_documentation": absentee_reason_documentation,
        "absentee_birth_year": absentee_birth_year,
        "absentee_telephone": absentee_telephone,
        "absentee_email": absentee_email,
        "absentee_street_address": absentee_street_address,
        "absentee_unit": absentee_unit,
        "absentee_city": absentee_city,
        "absentee_state": absentee_state,
        "absentee_zip": absentee_zip,
        # "delivery_state_country": delivery_state_country,
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
    registrar_address: str = localitiesAndReasons.localities[request.form[
        'election__locality_gnis']]['email']
    return data, registrar_address


def build_pdf(data: Dict[str, str], registrar_address: str):
    id: str = hashlib.md5(data).hexdigest()[:10]
    name: str = data['absentee_first_name'] + ' ' + data['absentee_middle_name'] + \
        ' ' + data['absentee_last_name'] + ', ' + data['absentee_suffix']
    write_fillable_pdf(data, id)
    return id, registrar_address, name


def email_registrar(id: str, registrar_address: str, absentee_name: str):
    # TODO: test
    # TODO: Way to keep one server open to minimize SMTP connections over and over again?
    yagmail.SMTP(GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD).send(
        to=registrar_address,
        subject=f'Absentee Ballot Request from {absentee_name}',
        contents='Please find attached an absentee ballot request submitted '
        + f'on behalf of {absentee_name}.',
        attachments=f'applications/{id}.pdf',
        headers="X-AB-ID"
    )
