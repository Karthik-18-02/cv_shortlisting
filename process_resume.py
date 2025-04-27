# process_resume.py
from utils.resume_processor import extract_text_from_pdf, extract_candidate_info, process_job_descriptions
from utils.bert_matcher import BERTMatcher
import os

# Path to the uploaded resume and job descriptions CSV
resume_path = 'data/CVs/C1061.pdf'  # Path to the resume (can be replaced with the file path)
job_descriptions_csv_path = 'data/job_descriptions.csv'  # Path to the job descriptions CSV

# Initialize the BERT matcher
bert_matcher = BERTMatcher("bert-base-uncased")

# Step 1: Extract text from the resume
resume_text = extract_text_from_pdf(resume_path)

# Step 2: Extract candidate information (skills and qualifications)
candidate_info = extract_candidate_info(resume_text)

# Step 3: Process job descriptions from CSV
job_descriptions = process_job_descriptions(job_descriptions_csv_path)

# Step 4: Calculate match scores for each job title
results = []
for job in job_descriptions:
    score = bert_matcher.calculate_match_score(job['Cleaned Description'], candidate_info)
    results.append({'title': job['Job Title'], 'score': round(score, 4)})

# Step 5: Display match scores for all job titles
for result in results:
    print(f"Job Title: {result['title']}, Match Score: {result['score']}")

