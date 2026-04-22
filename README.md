# AI CV-Filter — Intelligent Resume Screening Automation

## Overview

Recruitment workflows often involve repetitive manual tasks such as downloading resumes, filtering candidates, and organizing applicant data. This project focuses on reducing manual effort, saving time, and minimizing fatigue by automating key steps in the hiring pipeline.

The AI CV-Filter is a Python-based web application that integrates email automation with structured filtering to help HR teams handle large volumes of resumes more efficiently.

In many organizations, HR teams spend a considerable amount of time performing routine tasks like downloading resumes from emails, sorting files, and applying basic filtering criteria. These activities are time-consuming, prone to errors, and add unnecessary cognitive load.


This project automates the initial stages of resume processing. It connects to Gmail, retrieves recent emails with attachments, filters relevant resume files, and prepares them for further processing. The system is designed to be modular so that more advanced AI-based filtering can be integrated later.

## Project Pipeline

### Entry Point

The application runs as a Python web app through:

```bash
python main.py
```

### Step 1: Download Resumes from Gmail

This step is triggered through a button 'Download from Gmail' in the user interface. It calls the function `GmailAccess.downloadAttachments()`.

The function connects to the Gmail API, fetches recent emails, and extracts attachments. It then filters files based on supported formats, specifically `.pdf` and `.docx`. Only valid resume files are passed to the HR dashboard for further use.

it stores files in Artifacts/email_attachment folder (can be specified by you using json mappings )

### Step 2: List Files 

triggered through button 'View Downloaded Files' in interface. it calls function `list_files()` from `main.py` .

this shows name of file and sender's email address and subject of incoming email.

this step is not completely necessary, it is onto you to view your downloaded files or not.

## System Architecture

At a high level, the system follows a simple flow where the user interacts with the web application, which communicates with the Gmail API, processes attachments, and returns filtered results to the interface.

## Tech Stack

The application is built using Python and integrates with the Gmail API. It is structured in a way that supports file handling and future extensions such as document parsing and AI-based evaluation. The web layer can be implemented using frameworks like Flask or FastAPI depending on the setup.

## Project Structure

```
.
├── main.py
├── gmail_access.py
├── utils/
├── data/
└── README.md
```

## Future Enhancements

The current implementation focuses on automation of data collection. Future work can extend this into deeper intelligence, including resume parsing, skill extraction, candidate scoring, and ranking. Integration with a database and analytics layer would further improve usability for HR teams.

## Limitations

At present, filtering is limited to file type validation and does not include semantic understanding of resume content. The system also depends on Gmail API access and proper configuration.

## Contribution

Contributions can focus on improving automation, adding intelligent filtering, or enhancing system performance and scalability.

## License

Add an appropriate license such as MIT depending on your preference.

## Project Philosophy

This project is built with an emphasis on practical impact. The objective is to create systems that reduce repetitive human effort and provide meaningful assistance in real workflows, rather than focusing only on theoretical or experimental AI implementations.
