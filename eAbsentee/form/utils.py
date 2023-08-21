import os
from yagmail import SMTP
from io import BytesIO
from random import choices as random_choices
from string import ascii_lowercase, digits
from flask import current_app
from datetime import date
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from dotenv import load_dotenv
from .models import db, User

# Change current working directory to directory 'functions.py' is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

file_paths = {
    'en': '../static/pdf/form2022.pdf',
    'es': '../static/pdf/spanish_form.pdf'
}

application_id_chars = ascii_lowercase + digits

class SystemOverloadError(Exception):
    pass
def application_process(request, group_code=None, lang=None, email_registrar=True):
    try:
        application_id = ''.join(random_choices(application_id_chars, k=24))
        print(f"processing application {application_id}")
        write_pdf(application_id, request, lang)
        email_pdf(application_id, request, email_registrar)
        add_to_database(application_id, request, group_code=group_code)
        if not current_app.debug:
            os.remove(f'{application_id}.pdf')
    except Exception as e:
        # Here, we assume any exception is due to system overload, this can be refined further
        raise SystemOverloadError("System Overload. Please try again later.") from e


def write_pdf(application_id, request, lang):
    today_date = date.today()

    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(163, 732, request.form['name_last'].title())
    can.drawString(405, 732, request.form['name_first'].title())
    can.drawString(172, 716, request.form['name_middle'].title())
    can.drawString(405, 716, request.form['name_suffix'])
    can.drawString(353, 700, '   '.join(request.form['ssn']))  # SSN
    can.drawString(504, 700, '  '.join(request.form['birthyear']))  # DOB

    if 'permanent_absentee' in request.form and request.form['permanent_absentee'] == 'on':
        can.drawString(340, 600, 'X') # Vote by Mail in All Elections Yes

        if 'permanent_absentee_primary_party' in request.form:
            if request.form['permanent_absentee_primary_party'] == "democratic":
                can.drawString(113, 567, 'X') # Dem Primary Ballots
            elif request.form['permanent_absentee_primary_party'] == "republican":
                can.drawString(221, 567, 'X') # Rep Primary Ballots
            elif request.form['permanent_absentee_primary_party'] == "no_primary":
                can.drawString(320, 567, 'X') # No Primary Ballots
        # else:
        #     # default to no primary
        #     can.drawString(317, 649, 'X') # No Primary Ballots
    else:
        can.drawString(371, 600, 'X') # Vote by Mail in All Elections No

        if 'election_type' in request.form:
            if request.form['election_type'] == "general_special":
                can.drawString(285, 639, 'X')  # Gen/Spec
            elif request.form['election_type'] == "democratic":
                can.drawString(405, 639, 'X') # Dem Prim
            elif request.form['election_type'] == "republican":
                can.drawString(504, 639, 'X') # Republican Primary

        if 'election_date' in request.form and request.form['election_date'] != "":
            election_date = date.fromisoformat(request.form['election_date']) # YYYY-MM-DD
            # `election_date` should be in `config.UPCOMING_ELECTIONS`
            can.drawString(196, 615, election_date.strftime('%m'))  # Month of Election
            can.drawString(245, 615, election_date.strftime('%d'))  # Day of Election
            can.drawString(289, 615, election_date.strftime('%Y'))  # Year of Election

        can.drawString(422, 615, request.form['registered_county'])  # City/County

        can.drawString(153, 525, request.form['ballot_address'])
        can.drawString(532, 525, request.form['ballot_apt'])
        can.drawString(133, 508, request.form['ballot_city'])
        can.drawString(320, 508, request.form['ballot_state'])
        can.drawString(405, 508, '    '.join(request.form['ballot_zip']))
        can.drawString(546, 508, request.form['ballot_country'])

    can.drawString(150, 682, request.form['address'])
    can.drawString(527, 682, request.form['apt'])
    can.drawString(136, 663, request.form['city'])
    can.drawString(393, 663, '     '.join(request.form['zip']))

    can.drawString(181, 432, request.form['former_name'])
    can.drawString(180, 416, request.form['former_address'])
    can.drawString(145, 400, request.form['former_city'])
    can.drawString(378, 400, request.form['former_state'])
    can.drawString(468, 400, '     '.join(request.form['former_zip']))
    # can.drawString(158, 448, 'City')
    # can.drawString(398, 448, 'State')
    # can.drawString(477, 448, '     '.join('20171'))
    if request.form['date_moved'] != '':
        date_moved = date.fromisoformat(request.form['date_moved']) # YYYY-MM-DD
        can.drawString(479, 416, date_moved.strftime('%m'))
        can.drawString(517, 416, date_moved.strftime('%d'))
        # can.drawString(300, 670, date_moved.strftime('%Y'))


    can.drawString(128, 301, 'X' if request.form.get(
        'assistance_check') == 'true' else '',)
    can.drawString(200, 249, request.form['assistant_name'])
    can.drawString(510, 248, request.form['assistant_phone'])
    can.drawString(200, 232, request.form['assistant_address'])
    can.drawString(550, 237, request.form['assistant_apt'])
    can.drawString(145, 218, request.form['assistant_city'])
    can.drawString(378, 218, request.form['assistant_state'])
    can.drawString(468, 218, '      '.join(request.form['assistant_zip']))
    can.drawString(210, 169, request.form['assistant_name'])
    if request.form['assistant_name']:
        can.drawString(450, 166, today_date.strftime('%m'))
        can.drawString(490, 166, today_date.strftime('%d'))
        can.drawString(540, 166, today_date.strftime('%y'))

    can.drawString(175, 464, request.form['email'])
    phonenumber = request.form['phonenumber']  # ddd-ddd-dddd
    # faster than regex:
    area_code = phonenumber[:3]
    central_office_code = phonenumber[4:7]
    line_number = phonenumber[8:]
    can.drawString(169, 481, "      ".join(area_code))
    can.drawString(255, 481, "      ".join(central_office_code))
    can.drawString(337, 481, "      ".join(line_number))

    can.drawString(260, 100, f'/s/ {request.form["signature"].strip().title()}')
    can.setFont('Helvetica', 10)
    can.drawString(320, 128, 'This absentee ballot request contains an electronic signature.')
    can.drawString(482, 100, today_date.strftime('%m'))
    can.drawString(522, 100, today_date.strftime('%d'))
    can.drawString(563, 100, today_date.strftime('%y'))

    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    existing_pdf = PdfFileReader(file_paths[lang], 'rb')
    output = PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    with open(f'{application_id}.pdf', 'wb') as output_pdf_file:
        output.write(output_pdf_file)


def add_to_database(application_id, request, group_code):
    if group_code is not None:
        group_code = group_code.lower()
    elif request.cookies.get('group'):
        group_code = request.cookies.get('group').lower()
    elif group_code is None:
        group_code = ''

    new_voter = User(
        application_id=application_id,
        name=(f'{request.form["name_first"].title()} {request.form["name_middle"].title()} {request.form["name_last"].title()}').replace(
            '  ', ' ').strip(),
        county=request.form['registered_county'],
        email=request.form['email'],
        phonenumber=request.form['phonenumber'],
        full_address=(request.form['address'] + ((' ' + request.form['apt']) if request.form['apt'] else '') + ', ' + request.form['city'] + ', ' + 'VA' + ' ' + request.form['zip']),
        ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
        group_code=group_code,
        lat=request.form['lat'] if 'lat' in request.form else "",
        long=request.form['long'] if 'long' in request.form else "",
        election_date=date.fromisoformat(request.form['election_date']) if request.form.get('election_date') else None,
    )

    db.session.add(new_voter)
    db.session.commit()

yag = SMTP(os.environ["GMAIL_SENDER_ADDRESS"], os.environ["GMAIL_SENDER_PASSWORD"])

def email_pdf(application_id, request, email_registrar):
    voter_email = request.form.get('email')
    recipients = set({voter_email, })
    if email_registrar:
        # if not current_app.debug or 'localhost' not in request.url_root:
        if 'localhost' not in request.url_root:
            registered_county = request.form['registered_county']
            if registered_county in current_app.config["LOCALITIES"]:
                recipients.add(current_app.config["LOCALITIES"][registered_county]['email'])

    yag.send(
        to=tuple(recipients),
        subject=f'Absentee Ballot Request - Applicant-ID: {application_id}',
        contents="""
        Registrar, attached is a voter application for absentee ballot. The voter sent it through eAbsentee.org and the voter is CC'd here. In compliance with the Virginia Dept. of Elections memo dated 9/19/2019 regarding electronically signed applications linked at <a href="https://eabsentee.org/guidance/">eabsentee.org/guidance/</a>, the signer was required to check a box affirming the Affirmation Statement of the Absentee Ballot Application. You can verify compliance with this requirement by inspecting <a href="https://eabsentee.org/form/">eabsentee.org/form/</a> which was used by this voter to generate the attached application.
        <br />
        Voter, no further action is required on your part. An absentee ballot will be mailed soon to the address you designated. To check on the status of your application, visit the <a href="https://vote.elections.virginia.gov/VoterInformation/Lookup/status">Virginia elections website</a>. Please allow the registrar at least five days to process it.
        <br />
        Votante, no necesita hacer nada más. Una papeleta para votar en ausencia será pronto enviada por correo al lugar designado. Para checar el estado de su aplicación, visite la página de las <a href="https://vote.elections.virginia.gov/VoterInformation/Lookup/status">elecciones de Virginia</a>. Favor de permitir al registrador, al mínimo, cinco días para tratarla.
        """,
        attachments=f'{application_id}.pdf',
    )
