from typing import List
import yagmail
from googleapiclient import discovery
import email
from httplib2 import Http
from oauth2client import file, client, tools
import re
import base64
import os
import sys

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def delete_emails() -> List:
    # Gets authentication json if it's been implemented before
    store = file.Storage('storage.json')
    creds = store.get()

    # If the credits don't work or don't exist, create them, and store them
    SCOPES = 'https://mail.google.com/'
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(
            'credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)


    # Builds connection to gmail client
    GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

    # user_id indicates to gmail that we are looking at OUR inbox
    user_id = 'me'
    label_id_one = 'SENT'

    # Connect to the api, request sent messages, then get a dictionary
    sent_messages = GMAIL.users().messages().list(
        userId=user_id, labelIds=[label_id_one], maxResults=1000).execute()

    message_list = sent_messages['messages']
    to_delete = []  # Final list of undeliverable messages

    for message in message_list:
        message_id = message['id']

        message = GMAIL.users().messages().get(
            userId=user_id, id=message_id
        ).execute()  # Fetch the message using API
        payload = message['payload']
        header = payload['headers']

        # Subject of Email
        for parts_of_header in header:
            if parts_of_header['name'] == 'Subject':
                if 'Request' in parts_of_header['value']:
                    to_delete.append(message_id)

        snippet = message['snippet']

    for email_id in to_delete:
        GMAIL.users().messages().delete(userId='me', id=email_id).execute()


delete_emails()
