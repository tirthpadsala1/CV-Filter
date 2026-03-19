from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import os
from utils.var import content
import sys
from pathlib import Path

global senderInfo


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Serve the main dashboard HTML"""
    return render_template('index.html')


@app.route('/api/download-gmail', methods=['POST'])
def downloadGmail():
    try:
        from src.pipelines.gmail_access import GmailAccess
        client = GmailAccess(
            secretsPath=content["tokenPath"],
            credentialsPath=content["credentialsPath"],
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
                
            files_info.append({
                    'name': filename,
                    'path': str(file_path),
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

        from src.pipelines.cv_classifier import CVClassifier
        classifier = CVClassifier(downloadFolder=content["emailAttachmentsPath"])
        
        cv_files = []
        res = classifier.DirectoryLoop()
        filtered_files = res["movedFiles"]
        for i in filtered_files:
            filename = str(os.path.basename(i))
            path = str(i)

            cv_files.append({
                "name":filename,
                "path":path
            })
        
        return jsonify({
            'success': True,
            'filtered_files': cv_files,
            'qualified_cvs': len(cv_files)
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
        from src.pipelines.ats_scorrer import ATSscorer
        
        scorer = ATSscorer(
            vectorDBpath=content["vectorDBPath"],
            collectionName="job_roles_DB",
            CVFolder=content["CVFolder"],
            HFToken=content["HFTOKEN"]
            )
        
        
        
        # Call your ATS scoring function here
        results = scorer.ATSscorrer_pipeline()

        scores = [i["score"] for i in results]
        
        # Sort by score descending
        scores = scores.sort(reverse=True)
        

        
        return jsonify({
            'success': True,
            'scores': scores,
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    os.makedirs(content["emailAttachmentsPath"], exist_ok=True)
    
    print(" Starting HR CV Dashboard Server...")
    print(f"Download folder: {os.path.abspath(content['emailAttachmentsPath'])}")
    print(f"Access dashboard at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)