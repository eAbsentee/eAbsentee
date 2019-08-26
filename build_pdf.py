#!/usr/bin/env pipenv run python
import pdfrw
import os
from typing import Dict
from flask import session
from datetime import date


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

    print(data['election_type'])
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


# for testing
# write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict)
