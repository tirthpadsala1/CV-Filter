from PyPDF2 import PdfReader
from docx import Document
import sys
import numpy as np
import os
from pathlib import Path

from utils.logging import logging
from utils.exception import CustomException
from utils.general import textExtract_docx, textExtract_pdf

from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sklearn.metrics.pairwise import euclidean_distances
import chromadb
from openai import OpenAI


class ATSscorer:
    
    def __init__(self, vectorDBpath: str, collectionName: str, CVFolder: str, HFToken: str):
        
        self.client = chromadb.PersistentClient(path=vectorDBpath)
        self.collection = self.client.get_collection(name=collectionName)
        
        
        cv_folder_path = Path(CVFolder)
        self.CVPaths = [
            str(path) for path in cv_folder_path.iterdir()
            if path.is_file() and path.suffix.lower() in ['.pdf', '.docx']
        ]
        
        logging.info(f"Found {len(self.CVPaths)} CV files to process")
        
        self.textSplitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        self.embeddingModel = SentenceTransformer("all-MiniLM-L6-v2")
        self.OpenAIClient = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=HFToken,
        )
        

        self.allowed_roles = {
            "computer_vision_engineer",
            "nlp_engineer",
            "devops_engineer",
            "web_developer",
            "fullstack_engineer",
            "frontend_engineer",
            "backend_engineer",
            "data_analyst",
            "data_scientist",
            "ai_engineer",
            "ml_engineer"
        }
    
    def get_text(self, CVPath: str):
      
        try:
          
            if CVPath.lower().endswith(".pdf"):
                CVtext = textExtract_pdf(CVPath)
                logging.info(f"func textExtract_pdf(): text found from {os.path.basename(CVPath)}")
                return CVtext
            
            elif CVPath.lower().endswith(".docx"):
                CVtext = textExtract_docx(CVPath)
                logging.info(f"func textExtract_docx(): text found from {os.path.basename(CVPath)}")
                return CVtext
            
            else:
                logging.warning(f"Unsupported file type: {CVPath}")
                return None
        
        except Exception as e:
            logging.error(f"Error in get_text() for {CVPath}: {e}")
            raise CustomException(e, sys)
    
    def get_cv_embeddings(self, CVtext: str):
        """Generate embeddings for CV text"""
        try:
            if not CVtext or CVtext.strip() == "":
                logging.warning("Empty CV text, cannot generate embeddings")
                return None
            
         
            splitted_text = self.textSplitter.split_text(CVtext)
            
            if not splitted_text:
                logging.warning("No text chunks created")
                return None
          
            embedded_vectors = self.embeddingModel.encode(
                splitted_text,
                batch_size=16,
                normalize_embeddings=True,
                show_progress_bar=False  
            ).tolist()
            
            if embedded_vectors:
                logging.info(f"func get_cv_embeddings(): created {len(embedded_vectors)} embedding vectors")
                return embedded_vectors
            else:
                logging.warning("No embeddings created")
                return None
        
        except Exception as e:
            logging.error(f"Error in get_cv_embeddings(): {e}")
            raise CustomException(e, sys)
    
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
    
    def load_role_embeddings(self, role: str):
       
        try:
            role_embeddings = self.collection.get(
                where={"roleID": role},
                include=["embeddings", "documents"]
            )
            
            if role_embeddings and role_embeddings.get('embeddings'):
                logging.info(f"func load_role_embeddings(): loaded embeddings for {role}")
                return role_embeddings
            else:
                logging.warning(f"No embeddings found for role: {role}")
                return None
        
        except Exception as e:
            logging.error(f"Error in load_role_embeddings(): {e}")
            raise CustomException(e, sys)
    
    def summary_LLM(self, roleText: str, CVText: str, role: str):
       
        try:
            if role == "false" or not CVText:
                return "No role match found"
            
            if isinstance(roleText, list):
                roleText = roleText[0] if roleText else ""
            
            system_prompt = f"""You are an ATS (Applicant Tracking System) analyzer. 
Your task is to analyze this CV against the requirements for a {role} position.

Provide:
1. MATCHED SKILLS: List skills from CV that match job requirements
2. MISSING SKILLS: Important requirements not found in CV
3. STRENGTHS: Key qualifications that make this candidate suitable
4. GAPS: Areas where candidate falls short
5. RECOMMENDATION: Short summary of fit (Good Match / Potential Match / Poor Match)

Be concise and specific."""
            
            user_prompt = f'''Requirements for {role}:
{roleText}

Candidate CV:
{CVText}'''
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            completion = self.OpenAIClient.chat.completions.create(
                model="openai/gpt-oss-20b:groq",
                messages=messages,
                temperature=0,
                max_tokens=500
            )
            
            summary = completion.choices[0].message.content.strip()
            
            if summary:
                logging.info(f"func summary_LLM(): generated summary for {role}")
                return summary
            else:
                return "No summary generated"
        
        except Exception as e:
            logging.error(f"Error in summary_LLM(): {e}")
            return f"Error generating summary: {str(e)}"
    
    def similarity_search(self, roleEmbeddings: list, CVEmbeddings: list):
       
        try:
            if not roleEmbeddings or not CVEmbeddings:
                logging.warning("Empty embeddings provided")
                return 0.0
            
            roleEmbeddings = np.array(roleEmbeddings)
            CVEmbeddings = np.array(CVEmbeddings)
            
            CV_centroid = CVEmbeddings.mean(axis=0)
            role_centroid = roleEmbeddings.mean(axis=0)
            
            cosine_sim = np.dot(CV_centroid, role_centroid) / (
                np.linalg.norm(CV_centroid) * np.linalg.norm(role_centroid)
            )
            
            euc_dist = 1 - ((euclidean_distances(roleEmbeddings, CVEmbeddings)) / 2)
            avg_euc_dist = np.mean(euc_dist)
            
            score = (0.7 * cosine_sim) + (avg_euc_dist * 0.3)
            
            score = float(np.round(score, 4) * 100)
            
            
            logging.info(f"func similarity_search(): calculated score = {score}")
            
            return score
        
        except Exception as e:
            logging.error(f"Error in similarity_search(): {e}")
            raise CustomException(e, sys)
    
    def ATSscorrer_pipeline(self):
        try:
            results = []
            
            
            logging.info(f"Processing {len(self.CVPaths)} CVs...")
            
            for i, cv_path in enumerate(self.CVPaths, 1):
                filename = os.path.basename(cv_path)
                logging.info(f"Processing {i}/{len(self.CVPaths)}: {filename}")
                
                try:
                    cv_text = self.get_text(cv_path)
                    
                    if not cv_text or cv_text.strip() == "":
                        logging.warning(f"Empty text for {filename}, skipping")
                        results.append({
                            "filename": filename,
                            "score": 0,
                            "summary": "Could not extract text from CV"
                        })
                        continue
                    
                    job_role = self.get_role(cv_text)
                    
                    cv_embeddings = self.get_cv_embeddings(cv_text)
                    
                    if not cv_embeddings:
                        logging.warning(f"Failed to generate embeddings for {filename}")
                        results.append({
                            "filename": filename,
                            "score": 0,
                            "summary": "Failed to generate embeddings"
                        })
                        continue
                    
                  
                    if job_role in self.allowed_roles:
                       
                        role_data = self.load_role_embeddings(job_role)
                        
                        if role_data and role_data.get('embeddings'):
                            
                            score = self.similarity_search(
                                role_data["embeddings"],
                                cv_embeddings
                            )
                            
                       
                            role_text = role_data.get("documents", [""])[0] if role_data.get("documents") else ""
                            summary = self.summary_LLM(role_text, cv_text, job_role)
                            
                            results.append({
                                "filename": filename,
                                "score": score,
                                "summary": summary,
                                "role": job_role  
                            })
                            
                            logging.info(f"{filename}: score={score}, role={job_role}")
                        else:
                            logging.warning(f"No role data found for {job_role}")
                            results.append({
                                "filename": filename,
                                "score": 0,
                                "summary": f"Role data not found for {job_role}",
                                "role": job_role
                            })
                    else:
    
                        results.append({
                            "filename": filename,
                            "score": 0,
                            "summary": f"Role not matched. LLM response: {job_role}",
                            "role": "unknown"
                        })
                        
                        logging.info(f"{filename}: No matching role")
                
                except Exception as cv_error:
                    logging.error(f"Error processing {filename}: {cv_error}")
                    results.append({
                        "filename": filename,
                        "score": 0,
                        "summary": f"Error: {str(cv_error)}",
                        "role": "error"
                    })
            
           
            results.sort(key=lambda x: x.get('score', 0), reverse=True)
            
            logging.info(f"Completed processing {len(results)} CVs")
            logging.info(f"Average score: {sum(r['score'] for r in results) / len(results):.2f}" if results else "No results")
            
            return results
        
        except Exception as e:
            logging.error(f"Error in ATSscorrer_pipeline(): {e}")
            raise CustomException(e, sys)

