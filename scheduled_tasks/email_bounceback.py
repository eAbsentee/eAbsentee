import yagmail
from apiclient import discovery
import email
from httplib2 import Http
from oauth2client import file, client, tools
import re
import base64
from keys import GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD
import os
from typing import List

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def bounceback_check() -> None:
    # Gets authentication json if it's been implemented before
    store = file.Storage('storage.json')
    creds = store.get()

    # If the credits don't work or don't exist, create them, and store them
    SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    # Builds connection to gmail client
    GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

    # user_id indicates to gmail when in the for loop that we are looking at OUR inbox
    user_id = 'me'

    label_id_one = 'INBOX'
    label_id_two = 'UNREAD'

    # We connect to the api, request unread messages from our account, and then get a dictionary.
    unread_messages = GMAIL.users().messages().list(
        userId=user_id, labelIds=[label_id_one, label_id_two]).execute()

    try:
        message_list = unread_messages['messages']
    except(Exception):
        return []

    final_list: List = []  # Final list of undeliverable messages which need to be covered

    for message in message_list:
        message_id = message['id']

        message = GMAIL.users().messages().get(
            userId=user_id, id=message_id).execute()  # Fetch the message using API
        payload = message['payload']
        header = payload['headers']

        to_append = True

        # Subject of Email
        for parts_of_header in header:
            if parts_of_header['name'] == 'Subject':
                msg_subject = parts_of_header['value']
                if 'Failure' in msg_subject:
                    continue
                else:
                    to_append = False

        if to_append is True:
            snippet = message['snippet']

            email_which_bounced_regex = re.search(
                r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?", snippet)
            email_which_bounced = email_which_bounced_regex.group(
                0) if email_which_bounced_regex else ""

            message = GMAIL.users().messages().get(userId=user_id,
                                                   id=message_id,
                                                   format='raw').execute()
            message_with_bytes = base64.urlsafe_b64decode(
                message['raw'].encode('ASCII'))
            email_object = email.message_from_bytes(message_with_bytes)
            email_object_as_string = email_object.as_string()

            application_id_object = re.search(
                r"Applicant-ID: \w{10}", email_object_as_string)
            application_id_string = application_id_object.group(
                0) if application_id_object else ""

            application_id = application_id_string[14:]  # Parses hash only
            if to_append and application_id_string:
                # This will create a dictonary item in the final list
                final_list.append([email_which_bounced, application_id])

        # This will mark the message as read
        GMAIL.users().messages().modify(userId=user_id, id=message_id, body={
            'removeLabelIds': ['UNREAD']}).execute()

    return final_list


def bounceback_email(final_list) -> None:
    """Email the form to the bounceback email """
    print('done')
    for pair in final_list:
        yagmail.SMTP(GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD).send(
            to='raunakdaga@gmail.com',
            # to='info@elections.virginia.gov',
            subject=f'Absentee Ballot Request (Bounceback) - Applicant-ID: {pair[1]}',
            contents='This email is being automatically delivered by the ' + \
            'eAbsentee absentee ballot application system. Our website, ' + \
            'eAbsentee.com, is used to request absentee ballots online in an ' + \
            ' easier manner. You can contact us at eAbsentee@gmail.com. ' + \
            'Thank you. Please find attached an absentee ballot request ' + \
            'which was unsuccesfully delivered to a registrar due to a ' + \
            'bounceback email. The email which caused the bounceback was ' + \
            f'{pair[0]}. We would apreciate if you could update us on the ' + \
            'correct registrar email for this locality.',
            attachments=f'../applications/{str(pair[1])}.pdf'
        )


bounceback_email(bounceback_check())
