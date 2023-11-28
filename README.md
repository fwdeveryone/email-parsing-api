# FWD:Everyone Email Parsing API

This repository contains:
 - A Python3 script for downloading a thread from any Gmail or G Suite inbox, and then parsing it using the FWD:Everyone email parsing API.
    - Note that while specific script only interfaces with G Suite, the actual endpoint can accept email from any provider &mdash; Outlook, Mailgun, Nylas, etc.
    - For JavaScript code that does the same thing, c.f. the source code for: https://api-demo.fwdeveryone.com/
 - Python and Ruby starter scripts for parsing locally-stored RFC 5322 messages.
    - Parse messages stored in a database, e.g. after they've been retrieved from somewhere like Mailgun or Postmark.
    - You can parse the .eml file you get when clicking 'Download message' on any Gmail message (except messages sent to yourself).

The email parsing API currently does two things:

- Accurately strips signatures and replies, so that:
    - Email threads can be cleanly displayed within web or mobile apps
    - Each message can be analyzed using NLP, which suddenly becomes accurate enough to be useful once you can actually tell who said what
- Renders each message in a 'normalized' subset of HTML, so that:
    - Messages can be styled with a consistent typography, for better readability and design
    - Messages can be used in contexts that typically only allow a limited subset of HTML, e.g. Reddit comments or GitHub issues

The email parsing API endpoint not require authentication, but non-authenticated requests have a low rate limit. To discuss production use, please email: `alex.krupp@fwdeveryone.com`.

To learn more, and for a web-based interactive demo of this API, visit https://api-demo.fwdeveryone.com.

## Downloading messages via the Gmail API

1. Clone this repository, e.g. with `git clone https://github.com/fwdeveryone/email-parsing-api.git`
2. Inside the repository folder, create and activate a Python virtualenv: `python3 -m venv . && . bin/activate`
3. Run `pip -r requirements.txt`
4. Go to https://console.cloud.google.com, and create a new project
5. Within this new project, configure the OAuth consent screen:
    1. In the left sidebar (on Desktop), go to 'APIs & Services' -> 'OAuth consent screen'.
    2. Click 'Configure consent screen'
    3. Under 'User Type', select 'Public' (so that you can use this script with any Gmail or G Suite account, not only G Suite accounts within your domain)
    4. Fill out the info on the first page.
    5. Click 'Add or Remove Scopes', and then check the box for '.../auth/userinfo.email' and then manually add 'https://www.googleapis.com/auth/gmail.readonly'
    6. Save the scopes, and then save the OAuth consent screen
6. Create an OAuth client ID:
    1. Under 'Application type', put 'Desktop application'.
    2. Download the client secret file, and save it into the same folder as this script under the name 'credentials.json'
7. Edit the `python-api-demo.py` file, and add the ID of the Gmail thread you want to retrieve to the `THREAD_ID` variable. 
    1. You can get the thread ID by running this js snippet in the Chrome developers console while viewing a Gmail thread: 
          `document.querySelector('[data-legacy-thread-id]').getAttribute('data-legacy-thread-id')`
8. Run the script with: `python3 python-api-demo.py`