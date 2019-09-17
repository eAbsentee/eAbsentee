import hashlib
import yagmail
import os
import openpyxl
import json
import sys
from openpyxl import load_workbook
from typing import Dict, List, Tuple
from flask import request, session
import datetime
from datetime import date
import io
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from subprocess import call
from keys import GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD, API_KEY

# import pdfrw || DEPRECATED


# Change current working directory to directory 'functions.py' is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

'''Deprecated, because we are no longer filling out by the fillable fields. Don't delete, however.'''
# Subtypes of pdfrw, needed to write to fillable app.
# ANNOT_KEY: str = '/Annots'
# ANNOT_FIELD_KEY: str = '/T'
# ANNOT_VAL_KEY: str = '/V'
# ANNOT_RECT_KEY: str = '/Rect'
# SUBTYPE_KEY: str = '/Subtype'
# WIDGET_SUBTYPE_KEY: str = '/Widget'

# Where the form lives
form_path: str = 'static/blankAppFillable.pdf'


def parse_data(request: request) -> Tuple[Dict[str, str], str]:
    """ Parse data from the form using the Flask request object and convert it
    into a dict format to allow it to be passed to the PDF filling methods."""
    todayDate: str = date.today().strftime("%m%d%y")

    campaign_name = ''
    if request.cookies.get('campaign'):
        with open('static/campaigns.json') as file:
            campaigns = json.load(file)
            campaign_id = campaigns[request.cookies.get('campaign')]
            campaign_name = campaign_id['name']

    group_code_req = ''
    if request.cookies.get('group'):
        group_code_req = request.cookies.get('group')

    data_dict: Dict[str, str] = {}  # Create outside of scope
    with open('static/localities_info.json') as file:
        localities = json.load(file)
        data_dict: Dict[str, str] = {
            'firstName': request.form['name__first'],
            'middleName': request.form['name__middle'],
            'lastName': request.form['name__last'],
            'suffix': request.form['name__suffix'],
            'ssn': '  '.join(request.form['name__ssn']),
            'reasonCode': '     '.join(request.form['reason__code']),
            'registeredToVote': localities[
                request.form['election__locality_gnis']
            ]['locality'],
            'supporting': request.form['reason__documentation'],
            'email': request.form.get('more_info__email_fax'),
            'address': request.form['address__street'],
            'apt': request.form['address__unit'],
            'city': request.form['address__city'],
            'zipCode': '   '.join(request.form['address__zip']),
            'ballotDeliveryAddress': request.form.get('delivery__street'),
            'ballotDeliveryCity': request.form.get('delivery__city'),
            'ballotDeliveryApt': request.form.get('delivery__unit'),
            'ballotDeliveryZip': '   '.join(request.form.get(
                'delivery__zip').replace('-', '')),
            'ballotDeliveryState': request.form.get('deliv-state'),
            'formerFullName': request.form.get('change__former_name'),
            'formerAddress': request.form.get('change__former_address'),
            'signature': '/S/ ' + request.form[
                'signature__signed'].replace('/S/', '', 1).strip(),
            'firstThreeTelephone': '   '.join(request.form.get('more_info__telephone').replace(
                '-', '').replace('(', '').replace(')', '').replace(' ', '')[0:3]),
            'secondThreeTelephone': '   '.join(request.form.get('more_info__telephone').replace(
                '-', '').replace('(', '').replace(')', '').replace(' ', '')[3:6]),
            'lastFourTelephone': '   '.join(request.form.get('more_info__telephone').replace(
                '-', '').replace('(', '').replace(')', '').replace(' ', '')[6:10]),
            'assistantCheck': 'X' if request.form.get(
                'assistance__assistance') == 'true' else '',
            'assistantFullName': request.form.get('assistant__name'),
            'assistantAddress': request.form.get('assistant__street'),
            'assistantSignature': request.form.get('assistant__sig'),
            'assistantApt': request.form.get('assistant__unit'),
            'assistantCity': request.form.get('assistant__city'),
            'assistantState': request.form.get('assistant__state'),
            'assistantZip': '   '.join(request.form.get(
                'assistant__zip').replace('-', '')),
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
            'countyCheck': 'X' if 'County' in localities[
                request.form['election__locality_gnis']
            ]['locality'] else '',
            'cityCheck': 'X' if 'City' in localities[
                request.form['election__locality_gnis']
            ]['locality'] else '',
            'dateMovedMonth': '   '.join(request.form.get('change__date_moved')[5:7]),
            'dateMovedDay': '   '.join(request.form.get('change__date_moved')[8:10]),
            'dateMovedYear': '   '.join(request.form.get('change__date_moved')[2:4]),
            'dateOfElectionMonth': '   '.join(request.form.get('election__date')[5:7]),
            'dateOfElectionDay': '   '.join(request.form.get('election__date')[8:10]),
            'dateOfElectionYear': '   '.join(request.form.get('election__date')[2:4]),
            'todaysDateMonth': '   '.join(todayDate[0:2]),
            'todaysDateDay': '   '.join(todayDate[2:4]),
            'todaysDateYear': '   '.join(todayDate[4:6]),
            'applicationIP': request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
            'emailMe': request.form.get('email_me'),
            'campaignCode': campaign_name,
            'groupCode': group_code_req
        }

    registrar_address: str = localities[request.form[
        'election__locality_gnis']]['email']

    return data_dict, registrar_address


def build_pdf(data: Dict[str, str], registrar_address: str) -> str:
    """Takes in an input of the data dictionary,
    along with the email address of the respective registrar.
    It calls set_session_keys, and then write_fillable_pdf,
    and then appends the data to the report, and then
    sends the registrar address to email_registrar."""

    set_session_keys(data, registrar_address)
    write_pdf(data)

    today_date: str = date.today().strftime("%m-%d-%y")
    report_path: str = f'reports/{today_date}.xlsx'

    data_for_report: List[str] = [
        session['name'],
        str(datetime.datetime.now().time()),
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
        data['campaignCode'],
        data['groupCode']
    ]

    append_to_report(report_path, data_for_report)
    emails_to_be_sent_to = [registrar_address]
    if data['emailMe'] == 'true':
        emails_to_be_sent_to.append(data['email'])
    return emails_to_be_sent_to


def set_session_keys(data: Dict[str, str], registrar_address: str) -> None:
    # id is first 10 characters of MD5 hash of dictionary
    id: str = hashlib.md5(repr(data).encode('utf-8')).hexdigest()[: 10]
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


def write_pdf(data: Dict[str, str]) -> None:
    packet = io.BytesIO()
    # Create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(180, 690, data['lastName'])  # LastName
    can.drawString(420, 690, data['firstName'])  # First Name
    can.drawString(185, 666, data['middleName'])  # Middle Name
    can.drawString(320, 666, data['suffix'])  # Suffix
    can.drawString(238, 638, data['genSpecCheck'])  # Gen/Spec Election
    can.drawString(383, 638, data['demPrimCheck'])  # Democratic Primary
    can.drawString(498, 638, data['repPrimCheck'])  # Republican Primary
    can.drawString(550, 675, data['ssn'])  # SSN
    can.drawString(207, 614, data['dateOfElectionMonth'])  # MonthOfElection
    can.drawString(251, 614, data['dateOfElectionDay'])  # Dayofelection
    can.drawString(291, 614, data['dateOfElectionYear'])  # YearOfElection

    can.drawString(331, 611, data['countyCheck'])  # REGISTERED COUNTY
    can.drawString(378, 611, data['cityCheck'])  # REGISTERED CITY
    can.drawString(425, 611, data['registeredToVote'])  # Registered locality

    can.drawString(189, 554, data['reasonCode'])
    can.setFont('Helvetica', 8)
    can.drawString(312, 555, data['supporting'])
    can.setFont('Helvetica', 12)
    can.drawString(423, 524, data['firstThreeTelephone'])  # FIRST 3 TELPEHONE
    can.drawString(480, 524, data['secondThreeTelephone'])  # SECOND 3 TELPEHONE
    can.drawString(537, 524, data['lastFourTelephone'])  # LAST 4 TELPEHONE
    can.drawString(178, 504, data['email'])

    can.drawString(171, 473, data['address'])
    can.drawString(516, 473, data['apt'])
    can.drawString(153, 453, data['city'])
    can.drawString(518, 453, data['zipCode'])  # ZIP CODE OF DELIVERY

    can.drawString(289, 424, data['deliverResidence'])  # DELIVERED TO RESIDENCE
    can.drawString(459, 424, data['deliverMailing'])  # DELIVERED TO MAILING
    can.drawString(289, 410, data['deliverEmail'])  # DELIVERED TO EMAIL
    # can.drawString(459, 410, data['deliverFax'])  # DELIVERED TO FAX
    can.drawString(168, 392, data['ballotDeliveryAddress'])
    can.drawString(532, 392, data['ballotDeliveryApt'])
    can.drawString(154, 372, data['ballotDeliveryCity'])
    can.drawString(317, 372, data['ballotDeliveryState'])
    can.drawString(442, 372, data['ballotDeliveryZip'])

    can.drawString(205, 340, data['formerFullName'])
    can.drawString(487, 340, data['dateMovedMonth'])  # MONTH MOVED
    can.drawString(528, 340, data['dateMovedDay'])  # DAY MOVED
    can.drawString(569, 340, data['dateMovedYear'])  # YEAR MOVED
    can.drawString(192, 320, data['formerAddress'])

    can.drawString(130, 292, data['assistantCheck'])  # Assistant checkbox
    can.drawString(170, 222, data['assistantFullName'])
    can.drawString(165, 202, data['assistantAddress'])
    can.drawString(513, 202, data['assistantApt'])
    can.drawString(150, 182, data['assistantCity'])
    can.drawString(363, 182, data['assistantState'])
    can.drawString(517, 182, data['assistantZip'])
    can.drawString(170, 162, data['assistantSignature'])

    can.drawString(247, 103, data['signature'])
    can.drawString(492, 103, data['todaysDateMonth'])  # Month Signed
    can.drawString(529, 103, data['todaysDateDay'])  # Day Signed
    can.drawString(569, 103, data['todaysDateYear'])  # Year Signed

    # Apply the changes
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)

    # Read the existing PDF (the first argument passed to this script)
    existing_pdf = PdfFileReader(form_path, "rb")
    output = PdfFileWriter()

    # Add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    # Finally, write "output" to a real file
    output.write(open(session['output_file'], "wb"))


def email_registrar(emails_to_send) -> None:
    """Email the form to the registrar of the applicant's locality. """
    yagmail.SMTP(GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD).send(
        to=(emails_to_send[0], emails_to_send[1]),
        subject='Absentee Ballot Request - Applicant-ID: ' +
        f'{session["application_id"]}',
        contents='Please find attached an absentee ballot request ' +
        f'submitted on behalf of {session["name"]}.',
        attachments=session['output_file']
    )


def application_process(request: request):
    email_registrar(build_pdf(*parse_data(request)))


def append_to_report(report_path: str, data: Dict[str, str]) -> None:
    """Add a row to the Excel spreadsheet with data from the application.
    If the spreadsheet doesn't already exist, create it. """
    if not os.path.isfile(report_path):
        create_report()
    report: openpyxl.workbook.Workbook = load_workbook(filename=report_path)
    worksheet: openpyxl.worksheet.worksheet.Worksheet = report.active
    worksheet.append(data)
    report.save(report_path)


def create_report() -> str:
    today_date: str = date.today().strftime("%m-%d-%y")

    report: openpyxl.workbook.Workbook = openpyxl.Workbook()
    sh: openpyxl.worksheet.worksheet.Worksheet = report.active
    sh['A1'] = 'Applicant Name'
    sh['B1'] = 'Time Submitted'
    sh['C1'] = 'Reason Code'
    sh['D1'] = 'Supporting Information'
    sh['E1'] = 'Registered to Vote Where'
    sh['F1'] = 'Email'
    sh['G1'] = 'Telephone Number'
    sh['H1'] = 'Address'
    sh['I1'] = 'IP Submitted From'
    sh['J1'] = 'Form ID'
    sh['K1'] = 'Campaign Code'
    sh['L1'] = 'Group Code'

    report_path: str = f'reports/{today_date}.xlsx'

    report.save(report_path)
    return report_path


def build_campaign_specific_form(campaign: str):
    with open('static/localities_info.json') as localities:
        with open('static/campaigns.json') as campaigns:
            localities_json = json.load(localities)
            campaigns_json = json.load(campaigns)
            ids_and_names = []
            campaignData = campaigns_json[campaign]
            county_nums = campaignData['county_nums']
            # for county_num in county_nums:
            # THIS IS OVERKILL! Just update campaigns with their own HTML file as we go for now.
            # We only have two campaigns anyways...


def add_to_campaign(request: request) -> None:
    call("git pull", shell=True)
    if request.form.get('api_key') == API_KEY:
        if request.form.get('campaign_name'):
            with open('static/campaigns.json') as file:
                campaigns = json.load(file)
                list_counties = request.form.get('county_codes').split()
                list_emails = request.form.get('campaign_email').split()
                new_campaign = {
                    request.form.get('campaign_code'): {
                        "county_nums": list_counties,
                        "name": request.form.get('campaign_name'),
                        "emails": list_emails
                    }
                }
                campaigns.update(new_campaign)
                with open('static/campaigns.json', 'w') as f:
                    json.dump(campaigns, f, indent=4, sort_keys=True)
        if request.form.get('group_name'):
            with open('static/groups.json') as file:
                groups = json.load(file)
                new_group = {
                    request.form.get('group_code'): {
                        "name": request.form.get('group_name'),
                        "email": request.form.get('group_email'),
                        "submissions": "0"
                    }
                }
                groups.update(new_group)
                with open('static/groups.json', 'w') as f:
                    json.dump(groups, f, indent=4, sort_keys=True)

    call("git add .", shell=True)
    call("git commit -m \"Added new campaign/group\"", shell=True)
    call("git push origin master", shell=True)


def get_ids_and_counties(request: request):
    ids_and_names = {}
    with open('static/campaigns.json') as file:
        campaigns = json.load(file)
        campaign_id = campaigns[request.cookies.get('campaign')]
        campaign_counties = campaign_id['county_nums']
        with open('static/localities_info.json') as localities_file:
            localities = json.load(localities_file)
            for county in campaign_counties:
                ids_and_names[county] = localities[county]['locality']
    print(ids_and_names)
    return ids_and_names


# Deprecated
# def write_fillable_pdf(data: Dict[str, str]) -> None:
#     """Fill out the PDF based on the data from the form. """
#     template_pdf: pdfrw.PdfReader = pdfrw.PdfReader(form_path)
#     template_pdf.Root.AcroForm.update(pdfrw.PdfDict(
#         NeedAppearances=pdfrw.PdfObject('true')))
#     annotations: pdfrw.PdfArray = template_pdf.pages[0][ANNOT_KEY]
#     for annotation in annotations:
#         if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
#             if annotation[ANNOT_FIELD_KEY]:
#                 key = annotation[ANNOT_FIELD_KEY][1:-1]
#                 if key in data.keys():
#                     annotation.update(
#                         pdfrw.PdfDict(V='{}'.format(data[key]))
#                     )
#     pdfrw.PdfWriter().write(session['output_file'], template_pdf)
