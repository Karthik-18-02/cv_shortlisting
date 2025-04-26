from src.candidate_shortlisting import shortlist_candidates
from src.data_preprocessing import preprocess_data
from src.job_matching import calculate_match_score_bert
from src.email_extraction import extract_text_from_pdf
from src.email_notification import send_email_notifications
import json
import os
import pandas as pd
import sys
sys.path.append('N:/CV_shortlisting/src')  # Add your src folder path here


# Load job descriptions
job_description_csv = "job_description.csv"  # Update with your job descriptions CSV path
job_df = pd.read_csv(job_description_csv, encoding='ISO-8859-1')
job_df = job_df.iloc[:, :2]
job_df['Processed_Description'] = job_df['Job Description'].str.replace(r'^( Description:|Description:|Job Description:)\s*', '', regex=True)
# Preprocess job descriptions
job_df['Processed_Description_'] = job_df['Processed_Description'].str.lower()
# Function to process the CV uploaded
def process_cv(pdf_path, threshold=0.75):
    # Step 1: Extract candidate information from PDF
    candidate_info = extract_text_from_pdf(pdf_path)
    
    # Step 2: Calculate match score for each job description
    match_scores = []
    for _, job_row in job_df.iterrows():
        job_description = job_row['Processed_Description_']
        job_title = job_row['Job Title']
        match_score = calculate_match_score_bert(job_description, candidate_info)
        match_scores.append((job_title, match_score))
    
    # Step 3: Shortlist candidates
    shortlisted_candidates = shortlist_candidates(match_scores, threshold)
    
    # Step 4: Send email notifications to shortlisted candidates
    send_email_notifications(shortlisted_candidates)
    
    return shortlisted_candidates

# Example usage
pdf_path = 'C1061.pdf'  # Replace with actual CV file path
shortlisted = process_cv(pdf_path)

# Save shortlisted candidates to JSON
with open('shortlisted_candidates.json', 'w') as f:
    json.dump(shortlisted, f)

# Print shortlisted candidates
print(shortlisted)
