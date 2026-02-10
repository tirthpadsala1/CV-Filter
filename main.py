from src.gmail_access import GmailAccess
import sys
from utils.logging import logging
from utils.exception import CustomException
from utils.var import token,SCOPES,downloadFolder

def gmailAccessPipeline(secretsPath = token , Scopes = SCOPES , MaxRecentEmails:int = 5 , FolderOfAttachments = downloadFolder):

   gmail = GmailAccess(
      secretsPath,
      Scopes

   )

   downloads = gmail.downloadAttachments()

   return downloads



