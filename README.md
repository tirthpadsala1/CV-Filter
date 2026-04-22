# AI CV-Filter — Intelligent Resume Screening Automation

## Overview

Recruitment workflows often involve repetitive manual tasks such as downloading resumes, filtering candidates, and organizing applicant data. This project focuses on reducing manual effort, saving time, and minimizing fatigue by automating key steps in the hiring pipeline.

The AI CV-Filter is a Python-based web application that integrates email automation with structured filtering to help HR teams handle large volumes of resumes more efficiently.

In many organizations, HR teams spend a considerable amount of time performing routine tasks like downloading resumes from emails, sorting files, and applying basic filtering criteria. These activities are time-consuming, prone to errors, and add unnecessary cognitive load.


This project automates the initial stages of resume processing. It connects to Gmail, retrieves recent emails with attachments, filters relevant resume files, and prepares them for further processing. The system is designed to be modular so that more advanced AI-based filtering can be integrated later.

## Project Pipeline and Code

### Entry Point

The application runs as a Python web app through:

```bash
python main.py
```

### Step 1: Download Resumes from Gmail

This step is triggered through a button 'Download from Gmail' in the user interface. It calls the function `GmailAccess.downloadAttachments()`.

`GmailAccess.gmailCOnnect()` - configurattion for connection with Gmail API from google cloud console. generates `credentials.json` , `tokens.json` files.

`GmailAccess.downloadAttachments()` - calls `GmailAccess.gmailCOnnect()` function to establish connection. requestes Gmail through Client secrets to download attachments with `.pdf` or `.docx` files. stores it into folder `email_attachments`. maps the path,sender,subjct and date in `mappig.json`.

### Step 2: List Files 

triggered through button 'View Downloaded Files' in interface. it calls function `list_files()` from `main.py` .

this shows name of file and sender's email address and subject of incoming email.

this step is not completely necessary, it is onto you to view your downloaded files or not.

### Step 3: Filter CVs

it is triggered through button 'Filter CVs' in interface. it calls function `CVClassifier.DirectoryLoop()` which is the wrapper of `CVClassifier` class.

`CVClassifier.textExtract_pdf()` & `CVClassifier.textExtract_docx()` - takes filepath as input. retrieves text from filepath (whether from .pdf files of .docx files) and return string of text from document.

`CVClassifier.classifier()` - takes filename and text as input. return score of CVs from predefined patterns and key words.

`CVClassifier.DirectoryLoop()` - the wrapper of `CVClassifier` class. takes path of folder with attachment as input . loop through each files calls above functions and classifies whether document is CV or not. moves CV files into `Artifacts\CVs` folder. deletes other files.

#### before next - you need to create a vector DB in your local storage by code given in `vector_DB.py` file as it contains vectors of required and expected skills and background for candidates

### Step 4: ATS scoring

triggered through button 'Calculate ATS Scoring' in interface once the filtration of CV is complete. it calls function `ATSscorrer.ATSscorrer_pipeline()` which is the wrapper of `ATSscorrer` class.

`ATSscorrer.get_text()` - takes path of file as input. returns text from given file.

`ATSscorrer.get_cv_embeddings()` - takes text as input and converts it into vector embeddings.

`ATSscorrer.get_role()` - takes text as input and identifies the role of given text here CV using LLM.

`ATSscorrer.load_role_embeddings()` - takes string of role as inputs, returns embeddings of requirements for that role from vector DB

`ATSscorrer.summary_LLM()` - takes role,text of CV and required skills as input , returns summary of what is matching and what is missing skill by comparision of applicant's CV's text and role requirement's text.

`ATSscorrer.similarity_search()` - takes vector embeddings of CV and required skills as input , compares both with methods like dot products of vectors, matrix multiplications , cosine similarity and ecludian distance between two and returns average score from 0 to 100.


## System Architecture

At a high level, the system follows a simple flow where the user interacts with the web application, which communicates with the Gmail API, processes attachments, and returns filtered results to the interface.

## Tech Stack

The application is built using Python and integrates with the Gmail API. It is structured in a way that supports file handling and future extensions such as document parsing and AI-based evaluation. The web layer can be implemented using frameworks like Flask. It also uses web Based LLM here, chat GPT model for improving result and performance.

## Future Enhancements

The current implementation focuses on automation of data collection. Future work can extend this into deeper intelligence, including resume parsing, skill extraction, candidate scoring, and ranking. Integration with a database and analytics layer would further improve usability for HR teams.


