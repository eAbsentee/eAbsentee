#!/usr/bin/env pipenv run python
import pdfrw
import os
from typing import Dict

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ANNOT_KEY: str = '/Annots'
ANNOT_FIELD_KEY: str = '/T'
ANNOT_VAL_KEY: str = '/V'
ANNOT_RECT_KEY: str = '/Rect'
SUBTYPE_KEY: str = '/Subtype'
WIDGET_SUBTYPE_KEY: str = '/Widget'

input_pdf_path: str = 'static/blankAppFillable.pdf'
# output_pdf_path: str = 'static/tempOutput.pdf'


data: Dict[str, str] = {
    "absentee_first_name": "Timothy",
    "absentee_middle_name": "Marcus",
    "absentee_last_name": "Jones",
    "absentee_suffix": "Ph.D.",
    "absentee_ssn": "8934",
    "election_type": "Democratic Primary",
    "election_date": "09 04 19",
    "election_locality": "Arlington County",
    "absentee_reason": "I am primarily and personally responsible for the care of a disabled/ill family member confined at home",
    "absentee_reason_documentation": "Mother",
    "absentee_birth_year": "1983",
    "absentee_telephone": "703123456",
    "absentee_email": "tmjones@edu.edu",
    "absentee_street_address": "1234 Fake Rd",
    "absentee_unit": "",
    "absentee_city": "Alexandria",
    "absentee_state": "Virginia",
    "absentee_zip": "20171",
    "delivery_destination": "residence address",
    "delivery_street_address": "",
    "delivery_unit": "",
    "delivery_city": "",
    "delivery_country": "",
    "delivery_state": "",
    "delivery_zip": "",
    "absentee_former_name": "",
    "absentee_former_address": "",
    "absentee_date_moved": "",
    "absentee_assistance": "",
    "assistant_signed": "",
    "assistant_name": "",
    "assistant_street_address": "",
    "assistant_unit": "",
    "assistant_city": "",
    "assistant_state": "",
    "assistant_zip": "",
    "assistant_signature": "",
    "absentee_agreement": "true",
    "absentee_signature_date": "08 24 19",
    "absentee_signature": "Timothy M. Jones"
}


def convert_data(data: Dict[str, str]):
    """Rename the keys in the dictionary to match the fields in the PDF. """
    data_dict = {
        # Data that is 1:1 transposable, no formatting required
        'firstName': data['absentee_first_name'],
        'middleName': data['absentee_middle_name'],
        'lastName': data['absentee_last_name'],
        'suffix': data['absentee_suffix'],
        'ssn': data['absentee_ssn'],
        'reasonCode': data['absentee_reason'],
        'supporting': data['absentee_reason_documentation'],
        'birthYear': data['absentee_birth_year'],
        'email': data['absentee_email'],
        'address': data['absentee_street_address'],
        'apt': data['absentee_unit'],
        'city': data['absentee_city'],
        'zipCode': data['absentee_zip'],
        'ballotDeliveryAddress': data['absentee_former_address'],
        'formerFullName': data['absentee_former_name'],
        'formerAddress': data['absentee_former_address'],
        'signature': data['absentee_signature'],

        # Data where formatting is required
        # 'dateOfElectionMonth': data[''],
        # 'dateOfElectionDay': data[''],
        # 'dateOfElectionYear': data[''],
        # 'todaysDateMonth': data[''],
        # 'todaysDateDay': data[''],
        # 'todaysDateYear': data['']
        'firstThreeTelephone': data['absentee_telephone'][0:3],
        'secondThreeTelephone': data['absentee_telephone'][3:6],
        'lastFourTelephone': data['absentee_telephone'][6:10],
        # 'deliverResidence': data[''],
        # 'deliverMailing': data[''],
        # 'deliverEmail': data[''],
        # 'deliverFax': data[''],
        # 'ballotDeliveryApt': data[''],
        # 'ballotDeliveryCity': data[''],
        # 'ballotDeliveryZip': data[''],
        # 'dateMovedMonth': data[''],
        # 'dateMovedDay': data[''],
        # 'dateMovedYear': data[''],
    }
    return data_dict


def write_fillable_pdf(data: Dict[str, str], outputID: str):
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
    pdfrw.PdfWriter().write(os.path.dirname(os.path.realpath(__file__))
                            + f'/applications/{outputID}.pdf', template_pdf)


# write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict)
