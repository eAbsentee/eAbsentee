#!/usr/bin/env pipenv run python
import pdfrw
import os
from typing import Dict
from flask import session

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

    data_dict = {
        'firstName': data['absentee_first_name'],
        'middleName': data['absentee_middle_name'],
        'lastName': data['absentee_last_name'],
        'suffix': data['absentee_suffix'],
        'ssn': data['absentee_ssn'],
        'reasonCode': data['absentee_reason'],
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
        'formerFullName': data['absentee_former_name'],
        'formerAddress': data['absentee_former_address'],
        'signature': data['absentee_signature'],
        'firstThreeTelephone': data['absentee_telephone'][0:3],
        'secondThreeTelephone': data['absentee_telephone'][3:6],
        'lastFourTelephone': data['absentee_telephone'][6:10],
        'assistantCheck': 'X' if data['absentee_assistance'] == 'true' else '',
        'deliverResidence': 'X' if data['delivery_destination'] == 'residence address' else '',
        'deliverMailing': 'X' if data['absentee_assistance'] == 'mailing address' else '',
        'deliverEmail': 'X' if data['absentee_assistance'] == 'true' else '',
        'deliverFax': 'X' if data['absentee_assistance'] == 'true' else '',
        'genSpecCheck': 'X' if data['election_type'] == 'General or Special Election' else '',
        'demPrimCheck': 'X' if data['election_type'] == 'Democractic Primary' else '',
        'repPrimCheck': 'X' if data['election_type'] == 'Republican Primary' else '',
        'countyCheck': 'X' if 'County' in data['election_locality'] else '',
        'cityCheck': 'X' if 'City' in data['election_locality'] else '',
        'dateMovedMonth': data['absentee_date_moved'][0:2],
        'dateMovedDay': data['absentee_date_moved'][3:5],
        'dateMovedYear': data['absentee_date_moved'][6:8],
        'dateOfElectionMonth': data['election_date'][0:2],
        'dateOfElectionDay': data['election_date'][3:5],
        'dateOfElectionYear': data['election_date'][6:8],
        'todaysDateMonth': data['absentee_signature_date'][0:2],
        'todaysDateDay': data['absentee_signature_date'][3:5],
        'todaysDateYear': data['absentee_signature_date'][6:8],
    }

    # print(data_dict)
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
