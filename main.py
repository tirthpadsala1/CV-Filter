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
        
        # Calculate scores
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