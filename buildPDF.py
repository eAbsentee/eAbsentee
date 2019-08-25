import pdfrw
import os
from typing import Dict

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

input_pdf_path = 'static/blankAppFillable.pdf'
output_pdf_path = 'static/tempOutput.pdf'
{
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

data_dict = {
    'reasonCode': 'A4',
    'lastName': 'Daga',
    'firstName': 'Raunak',
    'middleName': 'Bobana',
    'suffix': '',
    'ssn': '8888',
    'genSpecCheck': 'X',
    'demPrimCheck': 'X',
    'repPrimCheck': 'X',
    'countyCheck': 'X',
    'cityCheck': 'X',
    'dateOfElectionMonth': '05',
    'dateOfElectionDay': '05',
    'dateOfElectionYear': '05',
    'reasonCod': 'A4',
    'supporting': 'none',
    'birthYear': '2000',
    'email': 'raunakdaga@gmail.com'
}


def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    annotations = template_pdf.pages[0][ANNOT_KEY]
    for annotation in annotations:
        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
            if annotation[ANNOT_FIELD_KEY]:
                key = annotation[ANNOT_FIELD_KEY][1:-1]
                if key in data_dict.keys():
                    annotation.update(
                        pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                    )
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict)
