import json
import os.path
from pprint import pprint

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from apiclient.http import BatchHttpRequest
import requests

THREAD_ID = '181454409ba590cf'

OAUTH_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def _get_google_oauth_credentials():
    oauth_credentials = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        oauth_credentials = Credentials.from_authorized_user_file('token.json', OAUTH_SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not oauth_credentials or not oauth_credentials.valid:
        if oauth_credentials and oauth_credentials.expired and oauth_credentials.refresh_token:
            oauth_credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', OAUTH_SCOPES)
            oauth_credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(oauth_credentials.to_json())

    return oauth_credentials


def _get_list_of_message_ids_from_thread(gmail_client, THREAD_ID):
    message_id_list = []

    resp = gmail_client.users().threads().get(userId='me', id=THREAD_ID, format='metadata', metadataHeaders=[]).execute()

    for message in resp['messages']:
        message_id = message['id']
        message_id_list.append(message_id)

    return message_id_list


def _get_raw_messages_in_thread(gmail_client, message_id_list):
    raw_message_list = []

    def _raw_messages_callback(request_id, response, exception):
        if exception is not None:
            pprint(exception)
        raw_message_list.append(response)

    batch = BatchHttpRequest(batch_uri='https://www.googleapis.com/batch/gmail/v1/users')
    for message_id in message_id_list:
        message_id = message_id.strip('<>')
        batch.add(gmail_client.users().messages().get(userId='me', id=message_id, format='raw'), callback=_raw_messages_callback)
    batch.execute()

    return raw_message_list


def _get_uploader_email_address(gmail_client):
    resp = gmail_client.users().getProfile(userId='me').execute()
    uploader_email_address = resp['emailAddress']

    return uploader_email_address


if __name__ == "__main__":
    oauth_credentials = _get_google_oauth_credentials()
    gmail_client = build('gmail', 'v1', credentials=oauth_credentials)

    message_id_list = _get_list_of_message_ids_from_thread(gmail_client, THREAD_ID)
    raw_message_list = _get_raw_messages_in_thread(gmail_client, message_id_list)
    uploader_email_address = _get_uploader_email_address(gmail_client)

    post_request_body = { 'emailAddress': uploader_email_address, 'threadId': THREAD_ID, 'messages': [] }

    for raw_message in raw_message_list:
        message_dict = { 'raw': raw_message['raw'], 'internalDate': raw_message['internalDate'], 'id': raw_message['id'] }
        post_request_body['messages'].append(message_dict)

    url = 'https://api.fwdeveryone.com/api/v1/thread'
    resp = requests.post(url, json=post_request_body)

    pprint(resp.json())


    
    