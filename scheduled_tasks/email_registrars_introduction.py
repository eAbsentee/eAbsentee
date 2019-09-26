import json
import yagmail
from keys import GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD
import os
import time

# Sets CWD to whatever directory app.py is located in
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('..')


def email_report_api(registrar, email_address):
    yagmail.SMTP(GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD).send(
        # to=email_address,
        to='raunakdaga@gmail.com',
        subject=f'Introducing Vote Absentee Virginia',
        contents=f'Dear {registrar} Registrar,\n\n' +
        'In the near future, you may start receiving absentee ballot applications from this email address. I want to give you some background and, if you have any questions, to answer them.\n\n' +
        'The applications come from the website www.eAbsentee.org. It assists Virginia candidate campaigns and GOTV efforts to help people apply for absentee ballots. It is an upgrade of a website set up in 2015 in Virginia to do the same thing.\n\n' +
        'The website is sponsored by a not-for-profit 501(c)4 Virginia organization, Vote Absentee Virginia.\n\n' +
        'For reference, attached is guidance from the Virginia Department of Elections on electronically signed absentee ballot applications. Applications from our website conform with department requirements.\n\n' +
        'I hope you are pleased by this effort to help more citizens vote. If you have any questions or suggestions—such as if you prefer applications be sent to a different email address— please don’t hesitate to contact me.\n\n' +
        'Would you please be kind enough to respond to this email to let us know that you have received it and, if necessary, whitelisted our email address? Thank you.\n\n' +
        'Larry Rouvelas\n' +
        'President, Vote Absentee Virginia\n' +
        'Falls Church, VA\n' +
        '703-407-9938',
        attachments=f'static/eAbsentee guidance from VA Dept of Elections.jpg'
    )
    time.sleep(300)


with open('registrars_email.json') as file:
    registars_json = json.load(file)
    counties = registars_json.keys()
    for county in counties:
        print(county)
        email_report_api(registars_json[county]['locality'], registars_json[county]['email'])
