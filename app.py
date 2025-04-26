from flask import Flask, render_template, request, redirect, url_for
from config import Config
from utils.resume_processor import extract_text_from_pdf, extract_candidate_info, process_job_descriptions
from utils.bert_matcher import BERTMatcher
from utils.email_sender import send_email
import os
import re

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize BERT Matcher and load jobs
bert_matcher = BERTMatcher(Config.BERT_MODEL_NAME)
job_descriptions = process_job_descriptions(Config.JOB_DESCRIPTIONS_PATH)

@app.route('/')
def home():
    return render_template('index.html', upload_exists=True)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return redirect(request.url)
        file = request.files['resume']
        if file.filename == '':
            return redirect(request.url)
        # Validate extension
        if file and file.filename.lower().endswith(tuple(Config.ALLOWED_EXTENSIONS)):
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(save_path)
            # Extract and process resume
            resume_text = extract_text_from_pdf(save_path)
            candidate_info = extract_candidate_info(resume_text)
            # Compute match scores
            results = []
            for job in job_descriptions:
                score = bert_matcher.calculate_match_score(job['Cleaned Description'], candidate_info)
                shortlisted = score >= Config.THRESHOLD
                results.append({'title': job['Job Title'], 'score': round(score, 4), 'shortlisted': shortlisted})
            # Send emails to shortlisted candidates
            if any(r['shortlisted'] for r in results):
                email_match = re.search(r'[\w\.-]+@[\w\.-]+', resume_text)
                if email_match:
                    candidate_email = email_match.group(0)
                    for r in results:
                        if r['shortlisted']:
                            send_email(candidate_email, r['title'], Config)
            return render_template('results.html', results=results)
        return redirect(url_for('home'))
    return render_template('upload.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html', jobs=job_descriptions)

@app.route('/candidates')
def candidates():
    # TODO: replace with real persistence
    placeholder = []
    return render_template('candidates.html', candidates=placeholder)

if __name__ == '__main__':
    app.run(debug=True)
