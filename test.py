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

text = '''text:[Your Full Name]  
Senior AI Engineer | Machine Learning & MLOps  
[City, State] � [Phone Number] � [Email Address]  
[LinkedIn Profile URL] � [GitHub/Portfolio URL]  
Professional Summary  
Results -driven AI Engineer with 4+ years of experience designing, training, and deploying 
production -grade machine learning models. Expert in Natural Language Processing (NLP) 
and Computer Vision, with a strong focus on MLOps  and scalable cloud architectur e. Proven 
track record of reducing model inference latency by 30% and improving predictive accuracy 
in enterprise environments.  
 
Core Technical Skills  
Category  Technologies  
Languages  Python (Expert), SQL, C++, Bash  
Fram eworks  PyTorch, TensorFlow, JAX, Scikit -learn, Hugging Face  
AI/ML Domains  LLMs (Fine -tuning, RAG), Computer Vision, Reinforcement Learning  
Data & Cloud  AWS (SageMaker, Lambda), GCP (Vertex AI), PostgreSQL, MongoDB  
DevOps/MLOps  Docker, Kubernetes, MLflow, DVC, CI/CD, Weights & Biases  
 
Professional Experience  
Mid-Level AI Engineer | [Current Company Name]  
January 2023 � Present  
\uf0b7 Led the development of a Retrieval -Augmented Generation (RAG) pipeline  using 
LangChain and Pinecone, reducing customer support response times by 45%.  \uf0b7 Optimized large -scale transformer models  for production deployment using ONNX 
and TensorRT, achieving a 2.5x speedup in inference.  
\uf0b7 Architected an automated MLOps pipeline  using Kubeflow, reducing t he model 
deployment cycle from weeks to days.  
\uf0b7 Mentored 3 Junior Engineers  on best practices for data versioning and unit testing 
for ML code.  
Machine Learning Engineer | [Previous Company Name]  
June 2020 � December 2022  
\uf0b7 Developed and deployed a Computer Vi sion system  for real -time defect detection 
in manufacturing, reaching 98.5% mAP (mean Average Precision).  
\uf0b7 Implemented hyperparameter tuning strategies  (Optuna) that increased model F1 -
score by 12% across five core product features.  
\uf0b7 Collaborated with Data E ngineers  to build robust ETL pipelines processing 1TB+ 
of daily log data using Apache Spark.  
\uf0b7 Managed GPU resource allocation  within a shared cluster, reducing monthly cloud 
infrastructure costs by $4,000.  
 
Key Projects  
Open -Source Contribution: [Project Name/Link]  
\uf0b7 Developed a custom PyTorch implementation of [Specific Architecture, e.g., Vision 
Transformers] which gained 500+ stars on GitHub.  
\uf0b7 Reduced memory footprint by 20% through efficient gradient checkpointing.  
End-to-End LLM Application: [Project Name]  
\uf0b7 Built a personal finance assistant using Llama 3 and a vector database.  
\uf0b7 Integrated a FastAPI backend with a React frontend, deployed via Docker on AWS 
EC2.  
 
Education  
M.S. in Computer Science (Specialization in AI)  
University Name | Year of Graduation  
B.S. in Software Engineering  
University Name | Year of Graduation  
 Certifications  
\uf0b7 AWS Cer tified Machine Learning � Specialty  
\uf0b7 DeepLearning.AI TensorFlow Developer Specialization  
\uf0b7 NVIDIA Graduate Fellow (Optional/Honors)'''

def part3(text):

      scorer = ATSscorer(
            vectorDBpath=content["vectorDBPath"],
            collectionName="job_roles_DB",
            CVFolder=content["CVFolder"],
            HFToken=content["HFTOKEN"]
            )
      
      results = scorer.get_role(text)
      print(results)



if __name__=="__main__":

    part3(text)
   

