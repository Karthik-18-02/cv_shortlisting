# app.py
from flask import Flask, render_template, request, redirect, url_for
from config import Config
from utils.resume_processor import extract_text_from_pdf, extract_candidate_info, process_job_descriptions
from utils.bert_matcher import BERTMatcher
import os

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize BERT Matcher and load job descriptions
bert_matcher = BERTMatcher(Config.BERT_MODEL_NAME)
job_descriptions = process_job_descriptions(Config.JOB_DESCRIPTIONS_PATH)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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

            # Compute match scores for job descriptions
            results = []
            for job in job_descriptions:
                score = bert_matcher.calculate_match_score(job['Cleaned Description'], candidate_info)
                shortlisted = score >= Config.THRESHOLD  # Check if score meets threshold
                if shortlisted:
                    results.append({'title': job['Job Title'], 'score': round(score, 4), 'shortlisted': shortlisted})

            # Redirect to the results page with dynamic data
            return render_template('results.html', results=results)

        return redirect(url_for('home'))  # Redirect back to home if file is invalid
    
    return render_template('upload.html')  # Render the upload page when visited normally

@app.route('/show_results', methods=['GET', 'POST'])
def show_results():
    # Fetch all PDFs in the upload folder
    uploaded_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
    
    all_results = []
    
    # Process each file in the upload folder
    for file_name in uploaded_files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        
        # Extract text from each PDF
        resume_text = extract_text_from_pdf(file_path)
        candidate_info = extract_candidate_info(resume_text)
        
        # Calculate match scores for job descriptions
        results = []
        for job in job_descriptions:
            score = bert_matcher.calculate_match_score(job['Cleaned Description'], candidate_info)
            shortlisted = score >= Config.THRESHOLD  # Check if score meets threshold
            if shortlisted:
                results.append({'title': job['Job Title'], 'score': round(score, 4), 'shortlisted': shortlisted})
        
        # Add the results for this resume (file)
        all_results.append({'file': file_name, 'results': results})

    # Search functionality
    search_query = request.form.get('search', '').lower()  # Get search query from form
    if search_query:
        # Filter results based on the search query (case-insensitive)
        all_results = [data for data in all_results if search_query in data['file'].lower()]

    # Render the results page with the filtered results
    return render_template('results.html', results_data=all_results)

@app.route('/jobs')
def jobs():
    return render_template('jobs.html', jobs=job_descriptions)

@app.route('/candidates')
def candidates():
    # Placeholder for candidate listing
    placeholder = []
    return render_template('candidates.html', candidates=placeholder)

if __name__ == '__main__':
    app.run(debug=True)
