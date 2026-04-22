from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import os
from itertools import zip_longest
from utils.var import content
from utils.logging import logging
import sys
from datetime import datetime
import json
from pathlib import Path


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

        
        download_info = client.downloadAttachments()

        
        
        with open(content["MapPath"] , 'r') as f:
            mapping_data = json.load(f)

        files_info = []
        for file in mapping_data:
        
            if file['date/time'] == f"{datetime.now().strftime('%m_%d_%Y')}":
            
                files_info.append({
                        'name': os.path.basename(file["path"]),
                        'path': file["path"],
                        'sender': file["sender"],
                        'subject': file["subject"]
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

        with open(content["MapPath"] , 'r') as f:
            senders = json.load(f) 

        for path in senders["path"]:
            if not os.path.exists(path):
                senders = [s for s in senders if s["path"] != path]

        if not os.path.exists(content["emailAttachmentsPath"]):
            os.makedirs(content["emailAttachmentsPath"])

        
        
        files_info = []
        for file in senders:
        
        
            
            files_info.append({
                    'name': os.path.basename(file["path"]),
                    'path': file["path"],
                    'sender': file["sender"],
                    'subject': file["subject"],
                    'type': 'New downloaded'
                })
        

        cv_folder = content["CVFolder"]
        if os.path.exists(cv_folder):
            for filename in os.listdir(cv_folder):
                file_path = cv_folder + filename
                for sender in senders:
                    if filename == os.path.basename(sender["path"]):
                        sender = sender["sender"]
                        subject = sender["subject"]
                if os.path.isfile(file_path):
                    files_info.append({
                        'name': filename,
                        'sender': sender if sender else 'Unknown',
                        'subject': subject if subject else 'No Subject',
                        'path': str(file_path),
                        'type': 'Existing CV'
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
       
        requested_path = request.args.get('path')
        if not requested_path:
            return jsonify({'success': False, 'error': 'No path provided'}), 400

       
        filename = os.path.basename(requested_path)

       
        attachments_dir = Path(content["emailAttachmentsPath"])
        cv_dir = Path(content["CVFolder"])

       
        file_in_attachments = attachments_dir / filename
        file_in_cv = cv_dir / filename

        if file_in_attachments.exists():
            return send_file(str(file_in_attachments))
        
        if file_in_cv.exists():
            return send_file(str(file_in_cv))

        # 4. If not found in either
        return jsonify({'success': False, 'error': f' {requested_path} or {filename} not found in allowed folders'}), 404

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/filter-cvs', methods=['POST'])
def filter_cvs():
    try:
        from src.pipelines.cv_classifier import CVClassifier

        sender_map = {}
        map_path = os.path.join(content["emailAttachmentsPath"], '_sender_map.json')
        if os.path.exists(map_path):
            with open(map_path, 'r') as mf:
                sender_map = json.load(mf)
        
        
        
        classifier = CVClassifier(downloadFolder=content["emailAttachmentsPath"])
        
       
        result = classifier.DirectoryLoop()
        
        filtered_files = []
        existing_files = []

        if len(result["existingFiles"]) >= 0:
            for path in result["existingFiles"]:
                 existing_files.append(
                    {
                        "path":str(path),
                        "name":os.path.basename(path),
                        'sender': sender_map.get(path, {}).get('sender', 'Unknown'),
                        'subject': sender_map.get(path, {}).get('subject', 'No Subject'),
                        "type":'Existing CV'
                    }
                )
            
        if len(result["movedFiles"]) >= 0:
            for path in result["movedFiles"]:
                filtered_files.append(
                    {
                        "path":str(path),
                        "name":os.path.basename(path),
                        "type":'Filtered CV'
                    }
                )

        logging.info(f"filtered files:{filtered_files} , existing files:{existing_files}")
        
        return jsonify({
            'success': True,
            'filtered_files': filtered_files,
            'existing_files': existing_files,
            'qualified_cvs': len(filtered_files),
            'total_processed': len(filtered_files)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/calculate-ats', methods=['POST'])
def calculate_ats():
    """
    Calculate ATS scores for filtered CVs
    
    Returns:
        JSON with ATS scores sorted by match percentage
    """
    try:
        
        from src.pipelines.ats_scorrer import ATSscorer

        scorer = ATSscorer(
            vectorDBpath=content["vectorDBPath"],
            collectionName="job_roles_DB",
            CVFolder=content["CVFolder"],
            HFToken=content["HFTOKEN"]
        )
        
       
        results = scorer.ATSscorrer_pipeline()
        
        if not results:
            return jsonify({
                'success': True,
                'scores': [],
                'total_cvs': 0,
                'message': 'No CVs found to process'
            })
        
        sorted_results = sorted(
            results,
            key=lambda x: x.get('score', 0),
            reverse=True 
        )
        
        def parse_summary(summary_text):
            """Extract structured data from LLM summary"""
            matched_skills = []
            missing_skills = []
            recommendation = ""
            
            if not summary_text or summary_text == "":
                return matched_skills, missing_skills, recommendation
            
            lines = summary_text.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                
                if 'MATCHED SKILLS' in line.upper():
                    current_section = 'matched'
                elif 'MISSING SKILLS' in line.upper():
                    current_section = 'missing'
                elif 'RECOMMENDATION' in line.upper():
                    current_section = 'recommendation'
                elif current_section == 'matched' and line and not line.startswith(('2.', '3.', '4.', '5.')):
    
                    skills = [s.strip() for s in line.replace('-', '').split(',') if s.strip()]
                    matched_skills.extend(skills)
                elif current_section == 'missing' and line and not line.startswith(('3.', '4.', '5.')):
                    skills = [s.strip() for s in line.replace('-', '').split(',') if s.strip()]
                    missing_skills.extend(skills)
                elif current_section == 'recommendation' and line:
                    recommendation = line
            
            return matched_skills, missing_skills, recommendation
        
        formatted_scores = []
        for item in sorted_results:
            matched_skills, missing_skills, recommendation = parse_summary(
                item.get('summary', '')
            )
            
            formatted_scores.append({
                'name': item.get('filename', 'Unknown'),
                'path':item["path"],
                'ats_score': item.get('score', 0),
                'summary': item.get('summary', ''),
                'matched_skills': matched_skills if matched_skills else ['N/A'],
                'missing_skills': missing_skills if missing_skills else ['N/A'],
                'recommendation': recommendation if recommendation else 'No recommendation available'
            })
        
        
        return jsonify({
            'success': True,
            'scores': formatted_scores,
            'total_cvs': len(formatted_scores),
            'top_score': formatted_scores[0]['ats_score'] if formatted_scores else 0,
            'average_score': round(sum(s['ats_score'] for s in formatted_scores) / len(formatted_scores), 2) if formatted_scores else 0
        })
    
    except KeyError as e:
        error_msg = f"Missing expected field in ATS results: {e}"

        return jsonify({
            'success': False,
            'error': error_msg,
            'error_type': 'KeyError'
        }), 500
    
    except ZeroDivisionError:
        error_msg = "No CVs available for ATS scoring"
        return jsonify({
            'success': False,
            'error': error_msg,
            'error_type': 'ZeroDivisionError'
        }), 400
    
    except Exception as e:
        error_msg = f"Error during ATS scoring: {str(e)}"
        
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }), 500


if __name__ == '__main__':
    os.makedirs(content["emailAttachmentsPath"], exist_ok=True)
    
    print(" Starting HR CV Dashboard Server...")
    print(f"Download folder: {os.path.abspath(content['emailAttachmentsPath'])}")
    print(f"Access dashboard at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)