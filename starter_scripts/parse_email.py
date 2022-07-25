import base64
import json
import requests
import uuid


# YOUR EMAIL ADDRESS HERE:
UPLOADER_EMAIL_ADDRESS = 'uploader_email_address@example.com'


def _get_base64_uuid():
    _uuid = uuid.uuid4()
    return base64.urlsafe_b64encode(_uuid.bytes)[0:-2].decode('utf-8')


# The thread ID provided by your email service provider, e.g. Gmail or Mailgun. If your ESP does not thread messages for you, provide your own UUID.
esp_thread_id = _get_base64_uuid()

post_request_body = {
    'emailAddress' : f'{UPLOADER_EMAIL_ADDRESS}',
    'threadId' : esp_thread_id,
    'messages' : []
}


with open("./message_1.txt") as file:
    message_1 = file.read()

raw_message_list = [ message_1, ]

for index, raw_message in enumerate(raw_message_list, start=0):
    message_uuid = _get_base64_uuid()
    encoded_stringified_raw_message = raw_message.encode('utf-8')
    base64_raw_message = base64.urlsafe_b64encode(encoded_stringified_raw_message).decode('utf-8')

    """ If you have an internalDate from your email service provider, use it here. (Your ESP has more data about how
    messages should be sorted within a thread than what is contained within the metadata for each message.) """
    current_message = { 'raw' : base64_raw_message, 'id' : message_uuid, 'internalDate': index }
    post_request_body['messages'].append(current_message)

uri = 'https://api.fwdeveryone.com/api/v1/thread'
resp = requests.post(uri, json=post_request_body, timeout=5)
print(resp.json())