from src.gmail_access import GmailAccess
from src.cv_classifier import CVClassifier
from utils.var import content

def part1():

        client = GmailAccess(
            secretsPath = content["tokenPath"],
            credentialsPath=  content["credentialsPath"],
            Scopes=['https://www.googleapis.com/auth/gmail.readonly'],
            FolderOfAttachments=content["emailAttachmentsPath"],
        )

        downloadedFiles,senders = client.downloadAttachments()

        return downloadedFiles , senders

def part2():
      
      classify = CVClassifier(
            downloadFolder = content["emailAttachmentsPath"]
      )

      classify.DirectoryLoop()


if __name__=="__main__":

    # part1()
    abc = part2()

