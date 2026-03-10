from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import os
from utils.var import content
import sys
from pathlib import Path

from src.gmail_access import GmailAccess

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Serve the main dashboard HTML"""
    return render_template('index.html')


@app.route('/api/download-gmail', methods=['POST'])
def downloadGmail():
    try:
        client = GmailAccess(
            secretsPath=content["tokenPath"],
            Scopes=['https://www.googleapis.com/auth/gmail.readonly'],
            FolderOfAttachments=content["emailAttachmentsPath"]
        )
        downloadedFiles , senderInfo = client.downloadAttachments()
        
        files_info = []
        for file in downloadedFiles:
            file_path = file['path']
            
            
            files_info.append({
                'name': file['filename'],
                'path': file_path,
                'sender': file.get('sender', 'Unknown'),
                'subject': file.get('subject', 'No Subject')
            })
        
        return jsonify({
            'success': True,
            'files': files_info,
            'count': len(files_info)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/list-files', methods=['GET'])
def list_files():
    try:
        if not os.path.exists(content["emailAttachmentsPath"]):
            os.makedirs(content["emailAttachmentsPath"])
            return jsonify({
                'success': True,
                'files': []
            })
        
        files_info = []
        for filename in os.listdir(content["emailAttachmentsPath"]):
            file_path = os.path.join(content["emailAttachmentsPath"], filename)
            
            if os.path.isfile(file_path) and filename.lower().endswith(('.pdf', '.doc', '.docx')):
                
                files_info.append({
                    'name': filename,
                    'path': file_path,
                })
        
        return jsonify({
            'success': True,
            'files': files_info
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/view-file', methods=['GET'])
def view_file():
    """
    Serve a file for viewing
    """
    try:
        file_path = request.args.get('path')
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        return send_file(file_path)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/filter-cvs', methods=['POST'])
def filter_cvs():
    """
    Filter CVs based on your criteria
    Replace this with your actual CV filtering logic
    """
    try:
        # TODO: Replace with your actual CV filtering code
        # Example: from your_cv_filter import filter_candidates
        
        # Get all CVs from download folder
        cv_files = []
        for filename in os.listdir(content["emailAttachmentsPath"]):
            file_path = os.path.join(content["emailAttachmentsPath"], filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.pdf', '.doc', '.docx')):
                cv_files.append({
                    'name': filename,
                    'path': file_path
                })
        
        # Call your filtering function here
        # filtered_results = your_filter_function(cv_files)
        
        # For now, return all files as example
        # Replace this with actual filtered results
        filtered_files = cv_files  # TODO: Replace with actual filtering
        
        return jsonify({
            'success': True,
            'filtered_files': filtered_files,
            'total_cvs': len(cv_files),
            'qualified_cvs': len(filtered_files)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/calculate-ats', methods=['POST'])
def calculate_ats():
    """
    Calculate ATS scores for CVs
    Replace this with your actual ATS scoring logic
    """
    try:
        # TODO: Replace with your actual ATS scoring code
        # Example: from your_ats_scorer import calculate_scores
        
        # Get filtered CVs (or all CVs if no filtering was done)
        cv_files = []
        for filename in os.listdir(content["emailAttachmentsPath"]):
            file_path = os.path.join(content["emailAttachmentsPath"], filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.pdf', '.doc', '.docx')):
                cv_files.append({
                    'name': filename,
                    'path': file_path
                })
        
        # Call your ATS scoring function here
        # scores = your_ats_function(cv_files)
        
        # Example response (replace with actual scores)
        scores = []
        for cv in cv_files:
            # TODO: Replace with actual ATS calculation
            import random
            score_data = {
                'name': cv['name'],
                'ats_score': random.randint(60, 95),  # Replace with actual score
                'matched_skills': ['Python', 'Machine Learning', 'SQL'],  # Replace with actual matched skills
                'missing_skills': ['AWS', 'Docker'],  # Replace with actual missing skills
                'path': cv['path']
            }
            scores.append(score_data)
        
        # Sort by score descending
        scores.sort(key=lambda x: x['ats_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'scores': scores
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    # Create download folder if it doesn't exist
    os.makedirs(content["emailAttachmentsPath"], exist_ok=True)
    
    print(" Starting HR CV Dashboard Server...")
    print(f"Download folder: {os.path.abspath(content["emailAttachmentsPath"])}")
    print(f"Access dashboard at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)