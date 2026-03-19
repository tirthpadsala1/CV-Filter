from PyPDF2 import PdfReader
from docx import Document
import sys
import numpy as np

import os
from pathlib import Path

from utils.logging import logging
from utils.exception import CustomException
from utils.general import textExtract_docx,textExtract_pdf

from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sklearn.metrics.pairwise import euclidean_distances
import chromadb
from openai import OpenAI

class ATSscorer:

    def __init__(self , vectorDBpath:str, collectionName:str , CVFolder:str , HFToken:str):

        self.client = chromadb.PersistentClient(path= vectorDBpath)
        self.collection = self.client.get_collection(name=collectionName)
        self.CVPaths = [path for path in Path(CVFolder).iterdir()]
        self.textSpillter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50,
                separators=["\n\n", "\n", ".", " ", ""]
            )
        self.embeddingModel = SentenceTransformer("all-MiniLM-L6-v2")
        self.OpenAIClient = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=HFToken,
        )

    
    def get_text(self , CVPath:str):

        try:

            if CVPath.endswith(".pdf"):
                CVtext = textExtract_pdf(CVPath)
                logging.info(f"func textExtract_pdf():  text found from {CVPath}. text:{CVtext[:20]}") 
                return CVtext

            elif CVPath.endswith(".docx"):
                CVtext = textExtract_docx(CVPath)
                logging.info(f"func textExtract_docx():  text found from {CVPath}. text:{CVtext[:20]}") 
                return CVtext

            else:
                logging.info(f"func get_text():  text not found from {self.CVPath}.")
                return False



        except Exception as e:
            logging.info(f"found error in function name: ATSscorer.get_cv_embeddings() , message{e}")
            raise CustomException(e,sys)
        

    def get_cv_embeddings(self, CVtext):

        try:
             

            
            if CVtext:

                splittedText = self.textSpillter.split_text(CVtext)
                
                embeddedVectors = self.embeddingModel.encode(
                    splittedText,
                    batch_size=16,
                    normalize_embeddings=True,
                    show_progress_bar=True
                ).tolist()

                if embeddedVectors:
                    logging.info(f"func get_cv_embeddings(): vectors for '{CVtext[:20]}....' created successfully. dimensions:{len(embeddedVectors)}")
                    return embeddedVectors
                
                else:
                    logging.info(f"func get_cv_embeddings(): vectors for '{CVtext[:20]}....' not created .")


        except Exception as e:
            logging.info(f"found error in function name: ATSscorer.get_cv_embeddings() , message{e}")
            raise CustomException(e,sys)
    
    
    def get_role(self, CVText):

        try:

            if CVText:

                prompt_roles = f'''You are an ATS classifier.

                    Your task:
                    - Identify the closest matching job role from the allowed list.
                    - If no match exists, return "false".

                    Allowed roles:
                    computer_vision_engineer
                    nlp_engineer
                    devops_engineer
                    web_developer
                    fullstack_engineer
                    frontend_engineer
                    backend_engineer
                    data_analyst
                    data_scientist
                    ai_engineer
                    ml_engineer

                    Return ONLY one role name or "false"..
                            '''

                messages=[
                    {"role": "system", "content": prompt_roles},
                    {"role": "user", "content": CVText}
                ]
                completion = self.OpenAIClient.chat.completions.create(
                model="openai/gpt-oss-20b:groq",
                messages = messages,
                temperature=0
                    )

                role = completion.choices[0].message.content.strip()

                if role:
                    summary =f"successfully got role:{role}" if role != "false" else "role not found or applying for other role."
                    logging.info(f"func get_role():- {summary}")

                    return role
            
        except Exception as e:
            logging.info(f"found error in function name: ATSscorer.get_cv_embeddings() , message{e}")
            raise CustomException(e,sys)
    
    def load_role_embeddings(self , role:str):
        try:

            roleEmbeddings = self.collection.get(
                where={"roleID":role},
                include=["embeddings" , "documents"]
            )

            if roleEmbeddings:
                logging.info(f"func load_role_embeddings(): successfully got role embeddings:{roleEmbeddings}")
                return roleEmbeddings
            
            else:
                return None

        except Exception as e:
            raise CustomException(e,sys)

    def summary_LLM(self, roleText:str, CVText:str, role:str):

        try:

            if role != False or role != "false":

                SystemPrompt = f"""You are an ATS (Applicant Tracking System) analyzer. 
                Your task is to analyze this CV against the requirements for a {role} position.

                Provide:
                1. MATCHED SKILLS: List skills from CV that match job requirements
                2. MISSING SKILLS: Important requirements not found in CV
                3. STRENGTHS: Key qualifications that make this candidate suitable
                4. GAPS: Areas where candidate falls short
                5. RECOMMENDATION: Short summary of fit (Good Match / Potential Match / Poor Match)

                Be concise and specific."""

                UserPrompt = f'''
                text of requriements for {role}:{roleText},,,,,
                text of candidate CV:{CVText}  '''

                messages = [
                {"role":"system" , "content":SystemPrompt},
                {"role":"user" , "content":UserPrompt}
                    ]

                completion = self.OpenAIClient.chat.completions.create(
                    model="openai/gpt-oss-20b:groq",
                    messages = messages,
                    temperature=0
                        )
            
                summary = completion.choices[0].message.content.strip()

                if summary:
                    logging.info(f"func summary_LLM(): summary by LLM:{summary}")
                    return summary

            else:

                return ""
        

        
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def similarity_searh(self, roleEmbeddings:list, CVEmbeddings:list):

        try:
            
            roleEmbeddings = np.array(roleEmbeddings)
            CVEmbeddings = np.array(CVEmbeddings)

            CVcentroid = CVEmbeddings.mean(axis=0)
            roleVectorscentroid = roleEmbeddings.mean(axis = 0)

            cosineSim = np.dot(CVcentroid , roleVectorscentroid) / (
                np.linalg.norm(CVcentroid) * np.linalg.norm(roleVectorscentroid)
            )

            ecu_dist = 1 - ((euclidean_distances(roleEmbeddings, CVEmbeddings)) / 2)
            avg_ecu_dist = np.mean(ecu_dist)

            score = ((0.7 * cosineSim) + (avg_ecu_dist * 0.3))

            score = float((np.round(score , 4)) * 100)

            if score:
                logging.info(f"func similarity_searh(): simlarity between vectors:{score}")

                return score
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def ATSscorrer_pipeline(self):

        try:

            Results = [ ]

            for CV in self.CVPaths:

                CVtext = self.get_text(str(CV))

                if not CVtext:
                    continue

                jobRole = self.get_role(CVtext)

                CVEmbeddings = self.get_cv_embeddings(CVtext)

                if jobRole in {"computer_vision_engineer",
                    "nlp_engineer",
                    "devops_engineer",
                    "web_developer",
                    "fullstack_engineer",
                    "frontend_engineer",
                    "backend_engineer",
                    "data_analyst",
                    "data_scientist",
                    "ai_engineer",
                    "ml_engineer"}:

                    RoleEmbeddings = self.load_role_embeddings(jobRole)
                    
                    score = self.similarity_searh(RoleEmbeddings["embeddings"] , CVEmbeddings)
                
                    summary = self.summary_LLM(RoleEmbeddings["documents"] , CVtext , jobRole)

                    Results.append({
                        "filename":str(os.path.basename(CV)),
                        "score":score,
                        "summary":summary
                    })

                else:

                    Results.append({
                        "filename":str(os.path.basename(CV)),
                        "score":0,
                        "summary":jobRole
                    })



            if Results:
                return Results

        except Exception as e:
            raise CustomException(e,sys)