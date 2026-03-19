# from src.gmail_access import GmailAccess
# from src.cv_classifier import CVClassifier
from utils.var import content
from src.pipelines.ats_scorrer import ATSscorer

# def part1():

#         client = GmailAccess(
#             secretsPath = content["tokenPath"],
#             credentialsPath=  content["credentialsPath"],
#             Scopes=['https://www.googleapis.com/auth/gmail.readonly'],
#             FolderOfAttachments=content["emailAttachmentsPath"],
#         )

#         downloadedFiles,senders = client.downloadAttachments()

#         return downloadedFiles , senders

# def part2():
      
#       classify = CVClassifier(
#             downloadFolder = content["emailAttachmentsPath"]
#       )

#       classify.DirectoryLoop()

def part3():

      scorer = ATSscorer(
            vectorDBpath=content["vectorDBPath"],
            collectionName="job_roles_DB",
            CVFolder=content["CVFolder"],
            HFToken=content["HFTOKEN"]
            )
      
      results = scorer.ATSscorrer_pipeline()
      print(results)



if __name__=="__main__":

    part3()
   

