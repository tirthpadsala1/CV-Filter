from chromadb.config import Settings
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.var import content

class JobRoles_VectorDB:
    
    def __init__(self, DBPath:str):

        self.client = chromadb.PersistentClient(
            path=DBPath,
            settings=Settings(anonymized_telemetry=False)
        )

        self.collection = self.client.get_or_create_collection(
            name="job_roles_DB",
            metadata={"description": "Job roles with requirements and skills"}
        )

        self.embeddingModel = SentenceTransformer("all-MiniLM-L6-v2")

        self.jobRoles ={
        
            "ml_engineer": {
                "title": "Machine Learning Engineer",
                "description": "Designs and implements machine learning models and pipelines",
                "required_skills": [
                    "Python programming", "Machine learning algorithms", "TensorFlow", "PyTorch", "Keras",
                    "Scikit-learn", "Data preprocessing", "Feature engineering", "Model deployment",
                    "ML pipelines", "Model optimization", "Hyperparameter tuning", "Cross-validation",
                    "Deep learning", "Neural networks", "CNN", "RNN", "Transformers", "BERT", "GPT",
                    "Computer vision", "NLP", "Time series analysis", "Reinforcement learning",
                    "MLflow", "Kubeflow", "Model versioning", "A/B testing", "Model monitoring"
                ],
                "tools_technologies": [
                    "Docker", "Kubernetes", "AWS SageMaker", "Azure ML", "Google AI Platform",
                    "Apache Spark", "Hadoop", "Kafka", "Airflow", "Jenkins", "Git", "Jupyter",
                    "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly", "OpenCV", "NLTK", "spaCy"
                ],
                "experience_levels": {
                    "entry": "0-2 years: Basic ML knowledge, coursework, internships",
                    "mid": "3-5 years: End-to-end ML projects, model deployment experience",
                    "senior": "6+ years: Leading ML initiatives, architecting solutions, mentoring"
                },
                "education": [
                    "Bachelor's in Computer Science, Mathematics, or related field",
                    "Master's or PhD in Machine Learning, AI, or related field (preferred for research roles)",
                    "Online certifications: Deep Learning Specialization, TensorFlow Developer Certificate",
                    "Publications in top conferences (for research positions)"
                ],
                "responsibilities": [
                    "Design and develop ML models for business problems",
                    "Build and maintain ML pipelines",
                    "Optimize model performance and accuracy",
                    "Deploy models to production",
                    "Monitor and maintain deployed models",
                    "Collaborate with data scientists and engineers",
                    "Stay updated with latest ML research"
                ],
                "soft_skills": [
                    "Problem-solving", "Analytical thinking", "Communication", "Team collaboration",
                    "Continuous learning", "Attention to detail", "Business acumen"
                ]
            },
            
            "ai_engineer": {
                "title": "AI Engineer",
                "description": "Builds and deploys AI systems and applications",
                "required_skills": [
                    "Python", "C++", "Java", "AI frameworks", "TensorFlow", "PyTorch", "JAX",
                    "Deep learning", "Reinforcement learning", "Generative AI", "GANs", "VAEs",
                    "Large Language Models", "LangChain", "LlamaIndex", "RAG systems", "Vector databases",
                    "Prompt engineering", "Fine-tuning", "AI agents", "Multi-modal AI", "Computer vision",
                    "Speech recognition", "Recommendation systems", "Predictive modeling",
                    "Model optimization", "ONNX", "TensorRT", "CUDA", "OpenCL"
                ],
                "tools_technologies": [
                    "Docker", "Kubernetes", "AWS", "GCP", "Azure", "LangChain", "LlamaIndex",
                    "ChromaDB", "Pinecone", "Weaviate", "Milvus", "Redis", "PostgreSQL",
                    "FastAPI", "Flask", "REST APIs", "GraphQL", "gRPC", "Redis", "RabbitMQ",
                    "Git", "CI/CD", "MLflow", "Weights & Biases", "Neptune.ai"
                ],
                "experience_levels": {
                    "entry": "0-2 years: AI coursework, projects, internships",
                    "mid": "3-5 years: Production AI systems, multiple successful deployments",
                    "senior": "6+ years: Architecting AI solutions, team leadership, innovation"
                },
                "education": [
                    "Bachelor's in Computer Science, AI, or related field",
                    "Master's in Artificial Intelligence or Machine Learning",
                    "PhD for research-intensive roles",
                    "AI certifications: AWS AI, Google AI, Microsoft Azure AI"
                ],
                "responsibilities": [
                    "Design and implement AI solutions",
                    "Integrate AI capabilities into applications",
                    "Optimize AI models for production",
                    "Build and maintain AI infrastructure",
                    "Research and implement new AI technologies",
                    "Collaborate with product and engineering teams",
                    "Ensure AI ethics and responsible AI practices"
                ],
                "soft_skills": [
                    "Innovation mindset", "Critical thinking", "Adaptability", "Cross-functional collaboration",
                    "Technical leadership", "Communication with stakeholders", "Ethical reasoning"
                ]
            },
            
        
            "data_scientist": {
                "title": "Data Scientist",
                "description": "Extracts insights from data using statistical and ML methods",
                "required_skills": [
                    "Python", "R", "SQL", "Statistics", "Probability", "Hypothesis testing",
                    "Experimental design", "A/B testing", "Regression analysis", "Classification",
                    "Clustering", "Dimensionality reduction", "Time series analysis", "Forecasting",
                    "Machine learning", "Deep learning", "Natural language processing",
                    "Feature engineering", "Data visualization", "Storytelling with data",
                    "Big data technologies", "Spark", "Hadoop", "Hive", "Pig"
                ],
                "tools_technologies": [
                    "Pandas", "NumPy", "SciPy", "Scikit-learn", "Statsmodels", "Matplotlib",
                    "Seaborn", "Plotly", "Tableau", "Power BI", "Looker", "Jupyter", "RStudio",
                    "SQL databases", "NoSQL databases", "Spark", "Hadoop", "Airflow",
                    "Git", "Docker", "AWS", "GCP", "Azure"
                ],
                "experience_levels": {
                    "entry": "0-2 years: Statistics degree, data analysis projects, internships",
                    "mid": "3-5 years: End-to-end data science projects, business impact",
                    "senior": "6+ years: Leading data science teams, strategic insights"
                },
                "education": [
                    "Master's or PhD in Statistics, Mathematics, Computer Science, or related field",
                    "Bachelor's with strong quantitative background and experience",
                    "Data Science bootcamps and certifications",
                    "Publications in peer-reviewed journals (for research roles)"
                ],
                "responsibilities": [
                    "Analyze complex datasets to extract insights",
                    "Develop statistical models and machine learning algorithms",
                    "Design experiments and A/B tests",
                    "Communicate findings to stakeholders",
                    "Collaborate with engineering and product teams",
                    "Stay current with latest research and techniques",
                    "Mentor junior data scientists"
                ],
                "soft_skills": [
                    "Curiosity", "Business acumen", "Communication", "Presentation skills",
                    "Critical thinking", "Problem-solving", "Collaboration", "Attention to detail"
                ]
            },
            
            "data_analyst": {
                "title": "Data Analyst",
                "description": "Analyzes data to support business decisions",
                "required_skills": [
                    "SQL", "Excel", "Python", "R", "Data cleaning", "Data wrangling",
                    "Data visualization", "Dashboard creation", "Statistical analysis",
                    "Descriptive statistics", "Exploratory data analysis", "Reporting",
                    "KPI tracking", "Business metrics", "Cohort analysis", "Funnel analysis",
                    "Customer segmentation", "Market basket analysis", "Trend analysis"
                ],
                "tools_technologies": [
                    "Tableau", "Power BI", "Looker", "Excel", "Google Sheets", "SQL databases",
                    "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly", "Jupyter",
                    "Mode Analytics", "Metabase", "Redash", "Superset", "QlikView"
                ],
                "experience_levels": {
                    "entry": "0-2 years: Data analysis coursework, internships, Excel skills",
                    "mid": "2-4 years: Independent analysis, dashboard creation",
                    "senior": "5+ years: Leading analysis initiatives, mentoring"
                },
                "education": [
                    "Bachelor's in Statistics, Mathematics, Economics, Computer Science, or related field",
                    "Data Analytics bootcamps and certifications",
                    "Google Data Analytics Certificate, IBM Data Analyst Certificate"
                ],
                "responsibilities": [
                    "Collect and clean data from various sources",
                    "Create dashboards and reports",
                    "Analyze data to identify trends and patterns",
                    "Present findings to stakeholders",
                    "Support data-driven decision making",
                    "Maintain data quality and integrity",
                    "Collaborate with business teams"
                ],
                "soft_skills": [
                    "Attention to detail", "Business acumen", "Communication", "Storytelling",
                    "Critical thinking", "Problem-solving", "Time management", "Curiosity"
                ]
            },
            
           
            "backend_engineer": {
                "title": "Backend Engineer",
                "description": "Builds server-side applications and APIs",
                "required_skills": [
                    "Python", "Java", "Go", "Node.js", "C#", "PHP", "Ruby",
                    "REST API design", "GraphQL", "gRPC", "Microservices architecture",
                    "Database design", "SQL", "NoSQL", "PostgreSQL", "MySQL", "MongoDB",
                    "Redis", "Elasticsearch", "Message queues", "RabbitMQ", "Kafka",
                    "Authentication", "Authorization", "OAuth", "JWT", "API security",
                    "Caching strategies", "Load balancing", "Scalability", "Performance optimization"
                ],
                "tools_technologies": [
                    "Docker", "Kubernetes", "AWS", "GCP", "Azure", "Terraform",
                    "CI/CD pipelines", "Jenkins", "GitLab CI", "GitHub Actions",
                    "Nginx", "Apache", "Linux", "Unix", "Postman", "Swagger",
                    "Prometheus", "Grafana", "ELK stack", "Datadog", "New Relic"
                ],
                "experience_levels": {
                    "entry": "0-2 years: CS degree, internships, basic API development",
                    "mid": "2-5 years: Production systems, scalable architectures",
                    "senior": "5+ years: System design, technical leadership, mentoring"
                },
                "education": [
                    "Bachelor's in Computer Science or related field",
                    "Bootcamp graduates with strong portfolios",
                    "Relevant certifications: AWS, Kubernetes, etc."
                ],
                "responsibilities": [
                    "Design and implement backend services",
                    "Build and maintain APIs",
                    "Optimize database queries and performance",
                    "Ensure security and data protection",
                    "Collaborate with frontend developers",
                    "Write clean, maintainable code",
                    "Participate in code reviews",
                    "Troubleshoot and debug issues"
                ],
                "soft_skills": [
                    "Problem-solving", "Analytical thinking", "Team collaboration",
                    "Communication", "Time management", "Attention to detail", "Adaptability"
                ]
            },
            
            "frontend_engineer": {
                "title": "Frontend Engineer",
                "description": "Builds user interfaces and web applications",
                "required_skills": [
                    "HTML5", "CSS3", "JavaScript", "TypeScript", "React", "Vue.js", "Angular",
                    "Responsive design", "Mobile-first design", "Cross-browser compatibility",
                    "State management", "Redux", "Vuex", "Context API", "Webpack", "Babel",
                    "CSS preprocessors", "SASS", "LESS", "Tailwind CSS", "Styled Components",
                    "REST API integration", "GraphQL clients", "Web performance optimization",
                    "Accessibility", "WCAG standards", "Progressive Web Apps", "PWA"
                ],
                "tools_technologies": [
                    "VS Code", "Chrome DevTools", "Figma", "Sketch", "Adobe XD",
                    "Jest", "React Testing Library", "Cypress", "Storybook",
                    "npm", "yarn", "Git", "GitHub", "GitLab", "Vite", "Parcel",
                    "Next.js", "Nuxt.js", "Gatsby", "Remix"
                ],
                "experience_levels": {
                    "entry": "0-2 years: Frontend projects, internships, portfolio",
                    "mid": "2-4 years: Complex applications, component libraries",
                    "senior": "4+ years: Architecture decisions, mentoring, best practices"
                },
                "education": [
                    "Bachelor's in Computer Science or related field",
                    "Frontend bootcamps with strong portfolios",
                    "Self-taught with demonstrated projects"
                ],
                "responsibilities": [
                    "Build responsive and accessible user interfaces",
                    "Implement designs from wireframes and mockups",
                    "Optimize applications for performance",
                    "Ensure cross-browser compatibility",
                    "Collaborate with designers and backend engineers",
                    "Write clean, maintainable code",
                    "Stay updated with frontend trends",
                    "Test and debug frontend code"
                ],
                "soft_skills": [
                    "Creativity", "Attention to detail", "Empathy for users",
                    "Collaboration", "Communication", "Adaptability", "Problem-solving"
                ]
            },
            
            "fullstack_engineer": {
                "title": "Full Stack Engineer",
                "description": "Works on both frontend and backend of applications",
                "required_skills": [
                    "Frontend: HTML, CSS, JavaScript, React/Vue/Angular",
                    "Backend: Python/Node.js/Java/Go, REST APIs, GraphQL",
                    "Database: SQL, NoSQL, ORM/ODM",
                    "Authentication, Authorization",
                    "Version control with Git",
                    "Deployment and DevOps basics",
                    "Testing: unit, integration, e2e",
                    "Security best practices",
                    "Performance optimization",
                    "Responsive design"
                ],
                "tools_technologies": [
                    "Full stack frameworks: Next.js, Nuxt.js, Django, Ruby on Rails, Laravel",
                    "Databases: PostgreSQL, MongoDB, MySQL, Redis",
                    "DevOps: Docker, CI/CD, cloud platforms",
                    "Testing: Jest, PyTest, Cypress, Selenium",
                    "Package managers: npm, pip, yarn",
                    "Project management: Jira, Trello, Asana"
                ],
                "experience_levels": {
                    "entry": "0-2 years: Full stack projects, internships",
                    "mid": "2-4 years: End-to-end feature development",
                    "senior": "4+ years: Architecture, technical leadership"
                },
                "education": [
                    "Bachelor's in Computer Science or related field",
                    "Full stack bootcamps with strong portfolios",
                    "Self-taught with comprehensive projects"
                ],
                "responsibilities": [
                    "Develop end-to-end features",
                    "Design and implement APIs",
                    "Build responsive user interfaces",
                    "Design database schemas",
                    "Deploy and maintain applications",
                    "Collaborate with cross-functional teams",
                    "Troubleshoot across the stack",
                    "Optimize application performance"
                ],
                "soft_skills": [
                    "Versatility", "Problem-solving", "Quick learning",
                    "Communication", "Adaptability", "Ownership", "Collaboration"
                ]
            },
            
            # ============== WEB DEVELOPMENT ROLES ==============
            "web_developer": {
                "title": "Web Developer",
                "description": "Builds and maintains websites and web applications",
                "required_skills": [
                    "HTML5", "CSS3", "JavaScript", "Responsive design", "Cross-browser compatibility",
                    "WordPress", "CMS platforms", "PHP", "MySQL", "Website optimization",
                    "SEO basics", "Web accessibility", "DOM manipulation", "AJAX", "Fetch API",
                    "Version control with Git", "FTP/SFTP", "cPanel", "Web hosting management"
                ],
                "tools_technologies": [
                    "VS Code", "Sublime Text", "Chrome DevTools", "Figma", "Adobe XD",
                    "WordPress", "Drupal", "Joomla", "Wix", "Squarespace", "Webflow",
                    "Bootstrap", "Tailwind CSS", "jQuery", "npm", "yarn", "Gulp", "Grunt",
                    "FileZilla", "Cyberduck", "cPanel", "phpMyAdmin"
                ],
                "experience_levels": {
                    "entry": "0-2 years: Web projects, freelance work, internships",
                    "mid": "2-4 years: Multiple websites, client projects",
                    "senior": "4+ years: Complex web applications, team leadership"
                },
                "education": [
                    "Bachelor's in Web Development, Computer Science, or related field",
                    "Web development bootcamps and certificates",
                    "Self-taught with strong portfolio"
                ],
                "responsibilities": [
                    "Build and maintain websites",
                    "Ensure responsive design across devices",
                    "Optimize websites for speed and SEO",
                    "Troubleshoot and debug issues",
                    "Collaborate with designers and content creators",
                    "Update and manage website content",
                    "Implement security measures",
                    "Stay updated with web technologies"
                ],
                "soft_skills": [
                    "Creativity", "Attention to detail", "Client communication",
                    "Time management", "Problem-solving", "Adaptability"
                ]
            },
            
            # ============== DEVOPS & CLOUD ROLES ==============
            "devops_engineer": {
                "title": "DevOps Engineer",
                "description": "Manages infrastructure, deployment, and operations",
                "required_skills": [
                    "CI/CD pipelines", "Jenkins", "GitLab CI", "GitHub Actions",
                    "Infrastructure as Code", "Terraform", "CloudFormation", "Ansible",
                    "Containerization", "Docker", "Kubernetes", "Helm",
                    "Cloud platforms", "AWS", "GCP", "Azure",
                    "Monitoring", "Prometheus", "Grafana", "ELK stack", "Datadog",
                    "Scripting", "Bash", "Python", "Go",
                    "Linux/Unix administration", "Networking", "Security",
                    "Version control", "Git", "Artifact management", "Nexus", "Artifactory"
                ],
                "tools_technologies": [
                    "Docker", "Kubernetes", "OpenShift", "Rancher",
                    "Jenkins", "GitLab CI", "CircleCI", "Travis CI", "ArgoCD",
                    "Terraform", "Pulumi", "Ansible", "Puppet", "Chef",
                    "AWS (EC2, ECS, EKS, Lambda, S3, RDS)",
                    "GCP (Compute Engine, GKE, Cloud Functions)",
                    "Azure (VMs, AKS, Functions)",
                    "Prometheus", "Grafana", "ELK", "Splunk", "Datadog",
                    "Nginx", "Apache", "HAProxy", "Istio", "Linkerd"
                ],
                "experience_levels": {
                    "entry": "0-2 years: Linux, scripting, basic cloud knowledge",
                    "mid": "2-4 years: CI/CD, containerization, cloud infrastructure",
                    "senior": "4+ years: Infrastructure architecture, automation at scale"
                },
                "education": [
                    "Bachelor's in Computer Science or related field",
                    "Cloud certifications: AWS, GCP, Azure",
                    "Kubernetes certifications: CKA, CKAD",
                    "DevOps bootcamps and workshops"
                ],
                "responsibilities": [
                    "Design and maintain CI/CD pipelines",
                    "Manage cloud infrastructure",
                    "Automate deployment processes",
                    "Monitor system performance and reliability",
                    "Ensure security and compliance",
                    "Optimize infrastructure costs",
                    "Troubleshoot production issues",
                    "Collaborate with development teams"
                ],
                "soft_skills": [
                    "Automation mindset", "Problem-solving", "Collaboration",
                    "Communication", "Documentation", "Calm under pressure"
                ]
            },
            
            # ============== SPECIALIZED AI ROLES ==============
            "nlp_engineer": {
                "title": "NLP Engineer",
                "description": "Specializes in natural language processing and understanding",
                "required_skills": [
                    "Python", "NLTK", "spaCy", "Transformers", "Hugging Face",
                    "BERT", "GPT", "RoBERTa", "T5", "LLaMA", "Mistral",
                    "Text preprocessing", "Tokenization", "Stemming", "Lemmatization",
                    "Word embeddings", "Word2Vec", "GloVe", "FastText",
                    "Named Entity Recognition", "Sentiment analysis", "Text classification",
                    "Machine translation", "Summarization", "Question answering",
                    "LangChain", "LlamaIndex", "RAG systems", "Vector databases",
                    "Prompt engineering", "Fine-tuning", "Model evaluation",
                    "Speech recognition", "Text-to-speech", "Speech-to-text"
                ],
                "tools_technologies": [
                    "Hugging Face Transformers", "Hugging Face Datasets", "Hugging Face Hub",
                    "LangChain", "LlamaIndex", "ChromaDB", "Pinecone", "Weaviate",
                    "spaCy", "NLTK", "Gensim", "TextBlob", "Stanford CoreNLP",
                    "TensorFlow", "PyTorch", "JAX", "CUDA",
                    "FastAPI", "Flask", "Docker", "Kubernetes",
                    "Weights & Biases", "MLflow", "Gradio", "Streamlit"
                ],
                "experience_levels": {
                    "entry": "0-2 years: NLP coursework, projects, internships",
                    "mid": "2-4 years: Production NLP systems, LLM applications",
                    "senior": "4+ years: Advanced NLP research, leading teams"
                },
                "education": [
                    "Master's or PhD in Computational Linguistics, NLP, or related field",
                    "Bachelor's with strong NLP experience",
                    "NLP certifications and specializations",
                    "Publications in ACL, EMNLP, NAACL (for research roles)"
                ],
                "responsibilities": [
                    "Develop NLP models for text processing",
                    "Build LLM-powered applications",
                    "Fine-tune language models",
                    "Implement RAG systems",
                    "Evaluate model performance",
                    "Stay current with NLP research",
                    "Collaborate with product and engineering teams",
                    "Optimize models for production"
                ],
                "soft_skills": [
                    "Research mindset", "Curiosity", "Analytical thinking",
                    "Communication", "Collaboration", "Continuous learning"
                ]
            },
            
            "computer_vision_engineer": {
                "title": "Computer Vision Engineer",
                "description": "Specializes in image and video processing",
                "required_skills": [
                    "Python", "C++", "OpenCV", "PIL", "scikit-image",
                    "Image processing", "Feature extraction", "Object detection",
                    "YOLO", "SSD", "Faster R-CNN", "EfficientDet",
                    "Image segmentation", "U-Net", "Mask R-CNN", "DeepLab",
                    "Face recognition", "Pose estimation", "Optical flow",
                    "3D vision", "Structure from motion", "Stereovision",
                    "GANs for image generation", "Style transfer", "Super-resolution",
                    "Video analysis", "Action recognition", "Tracking",
                    "TensorFlow", "PyTorch", "Keras", "CUDA", "cuDNN"
                ],
                "tools_technologies": [
                    "OpenCV", "PIL", "scikit-image", "albumentations", "imgaug",
                    "Detectron2", "MMDetection", "YOLOv5/v8", "MediaPipe",
                    "TensorFlow Object Detection API", "PyTorch Vision",
                    "ONNX", "TensorRT", "OpenVINO", "Core ML",
                    "Docker", "Kubernetes", "AWS Rekognition", "Google Vision API",
                    "Weights & Biases", "MLflow", "Gradio", "Streamlit"
                ],
                "experience_levels": {
                    "entry": "0-2 years: Computer vision coursework, projects",
                    "mid": "2-4 years: Production CV systems, multiple domains",
                    "senior": "4+ years: Advanced CV, research, team leadership"
                },
                "education": [
                    "Master's or PhD in Computer Vision, AI, or related field",
                    "Bachelor's with strong CV experience",
                    "Publications in CVPR, ICCV, ECCV (for research roles)"
                ],
                "responsibilities": [
                    "Develop computer vision models",
                    "Process and analyze image/video data",
                    "Optimize models for real-time performance",
                    "Deploy CV models to edge devices",
                    "Evaluate and improve model accuracy",
                    "Stay current with CV research",
                    "Collaborate with product and engineering teams"
                ],
                "soft_skills": [
                    "Visual thinking", "Problem-solving", "Innovation",
                    "Communication", "Collaboration", "Attention to detail"
                ]
            }
        }

    
    def prepare_document(self):

        documents = []

        for roleID , roleReqs in self.jobRoles.items():
            title = roleReqs.get('title',' ') 
            description = roleReqs.get('description' , ' ')
            requiredSkills = roleReqs.get('required_skills' , ' ')
            toolsTech = roleReqs.get('tools_technologies' , ' ')
            experience = roleReqs.get('experience_levels' , ' ')
            education = roleReqs.get('education' , ' ')
            responsibilities = roleReqs.get('responsibilities' , ' ')
            softSkills = roleReqs.get('soft_skills', ' ')

            text = f"""
            title:{title}

            description:{description}

            required skills:{requiredSkills}

            tool and technologies:{toolsTech}

            experience:{experience}

            education:{education}

            responsibilities:{responsibilities}

            soft skills:{softSkills}
        
            """

            documents.append({
                "roleID":roleID,
                "title":title,
                "text":text
            })

        return documents
    
    def Vectors(self):

        try:
            Docs = self.prepare_document()

            textSplitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50,
                separators=["\n\n", "\n", ".", " ", ""]
            )

            all_chunks = []
            all_metadata = []
            all_ids = []

            for doc in Docs:
                chunks = textSplitter.split_text(doc["text"])

                for i, chunk in enumerate(chunks):
                    all_chunks.append(chunk)

                    all_metadata.append({
                        "roleID": doc["roleID"],
                        "title": doc["title"]
                    })

                    all_ids.append(f"{doc['roleID']}_chunk_{i}")

            vectors = self.embeddingModel.encode(
                all_chunks,
                batch_size=16,
                normalize_embeddings=True,
                show_progress_bar=True
            ).tolist()

            return vectors, all_chunks, all_metadata, all_ids
        
        except Exception as e:
            print(e)

    def VDB(self):
            
        try:
            vectors, documents, metadata, ids = self.Vectors()

            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=vectors,
                metadatas=metadata
            )

            print("Job roles stored successfully")
        except Exception as e:
            print(e)