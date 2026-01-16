from __future__ import print_function
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import sys
import base64

from utils.logging import logging
from utils.exception import CustomException

class GmailAccess:

    def __init__(self, secretsPath:str, Scopes:list , MaxRecentEmails:int = 5, FolderOfAttachments:str = '../doc_downloads'):

        self.tokens = secretsPath
        self.Scopes = Scopes
        self.Recents = MaxRecentEmails
        self.FolderAttach = FolderOfAttachments


    def gmailConnect(self):

        logging.info("attempting to connect with Gmail API...")
        try:
            creds = None

            if os.path.exists(self.tokens):
                creds = Credentials.from_authorized_user_file(self.tokens , self.Scopes)

            logging.info(f"got credentials from,{self.tokens}.")

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())

                else:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json',self.Scopes)
                    creds = flow.run_local_server(port = 0)

                with open('token.json','w+') as token:
                    token.write(creds.to_json())

                logging.info(f"got credentials from local server.")


            return build('gmail','v1',credentials=creds)
        
        except Exception as e:
            logging.info("failed to connect with gmail..!")
            logging.info("found error:",e)
            raise CustomException(e,sys)
            
    

    def downloadAttachments(self):

        logging.info("attempting to download doc attachments form Gmail inbox....")

        try:
            service = self.gmailConnect()

            if not os.path.exists(self.FolderAttach):
                os.makedirs(self.FolderAttach)
                logging.info("created folder:",self.FolderAttach)

            
            results = service.users().messages().list(userId='me', q="has:attachment", maxResults=self.Recents).execute()

            if results:
                logging.info(f"got {self.Recents} emails with attachments(.pdf , .doc , .docx)...")
                
            messages = results.get('messages', [])

            if not messages:
                logging.info(f"no message with attachment found..")
                return []
            
            logging.info(f"retrived details of {len(messages)} recent mails from inbox...")

            all_downloaded = []
            logging.info(f"starting loop for retriving attachments..")

            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()

                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')

                def check_and_download_parts(parts, msg_id):
                    
                    downloaded = []

                    for part in parts:
                        if part.get('filename'):
                            filename = part['filename']

                            if filename.lower().endswith(('.pdf', '.docx', '.doc')):

                                if 'attachmentId' in part['body']:
                                    attachment = service.users().messages().attachments().get(
                                    userId='me',
                                    messageId=msg_id,
                                    id=part['body']['attachmentId']
                                    ).execute()

                                    file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                                    filepath = os.path.join(self.FolderAttach, filename)

                                    counter = 1
                                    base_name, extension = os.path.splitext(filename)
                                    while os.path.exists(filepath):
                                        filepath = os.path.join(self.FolderAttach, f"{base_name}_{counter}{extension}")
                                        counter += 1

                                    with open(filepath, 'wb') as f:
                                        f.write(file_data)

                                    downloaded.append({'filename': filename, 'path': filepath})
                                    logging.info(f"from:{sender}")
                                    logging.info(f" Downloaded: {filename}")

                        if 'parts' in part:
                            downloaded.extend(check_and_download_parts(part['parts'], msg_id))

                email_attachments = []
                if 'parts' in msg['payload']:
                    email_attachments = check_and_download_parts(msg['payload']['parts'], message['id'])

                if email_attachments:
                    all_downloaded.extend(email_attachments)

            logging.info(f"total file downloaded:{len(all_downloaded)}")

            return all_downloaded
        
        except Exception as e:
            logging.info(f"found error {e}")
            raise CustomException(e,sys)