import data_preprocessing as dp
import nlp_processing as np
import job_matching as jm
import os
import pandas as pd
import fitz  # PyMuPDF

# Define the folder where your PDF files are located
pdf_folder = 'data/CVs1'  # Assuming all the uploaded PDF files are here

# Process all uploaded PDF resumes and calculate match scores for each job description
def process_resumes_and_match_jobs(pdf_folder, job_descriptions_list):
    # Initialize an empty dictionary to store match scores for each CV
    match_scores_dict = {}

    # Loop through all PDF files (CVs) in the folder
    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            
            # Extract text from the CV PDF
            extracted_text = jm.extract_text_from_pdf(pdf_path)
            
            # Extract candidate information (skills, qualifications, experience) from the CV text
            candidate_info = jm.extract_candidate_info(extracted_text)
            
            # Initialize a list to hold the similarity scores for this CV against each job description
            match_scores = []
            
            # Loop through all job descriptions and calculate similarity score for this CV
            for job_desc_dict in job_descriptions_list:
                job_desc = job_desc_dict['Summary']  # Job description text
                match_score = jm.calculate_match_score_bert(job_desc, candidate_info)
                match_scores.append(match_score)
            
            # Store the similarity scores for this CV (use filename as the row)
            match_scores_dict[filename] = match_scores
    
    # Convert the dictionary into a DataFrame (rows: Job Titles, columns: CVs)
    job_titles = [job_desc_dict['Job Title'] for job_desc_dict in job_descriptions_list]
    match_scores_df = pd.DataFrame(match_scores_dict, index=job_titles)
    
    return match_scores_df
# Sample job description
# job_desc = "We are looking for a skilled Software Engineer with experience in Python, TensorFlow, and cloud computing."

# Process all the resumes in the folder and calculate match scores
match_scores = process_resumes_and_match_jobs(pdf_folder, jm.job_data)

# # Display candidates and their match scores
# for result in match_scores:
#     print(f"Candidate: {result['Candidate']}, Match Score: {result['Match Score']:.4f}")

print(match_scores)


import pandas as pd

# Threshold value
threshold = 0.75
cutoff_number = 10

# Function to shortlist candidates based on the threshold
def shortlist_candidates_by_threshold(match_scores_df, threshold):
    shortlisted_candidates = {}

    # Loop through each job title (row)
    for job_title in match_scores_df.index:
        # Get the CVs for this job title where the match score is above the threshold
        shortlisted_candidates[job_title] = match_scores_df.columns[
            match_scores_df.loc[job_title] >= threshold
        ].tolist()

    return shortlisted_candidates

# Get the shortlisted candidates
shortlisted_threshold = shortlist_candidates_by_threshold(match_scores, threshold)

# Display the shortlisted candidates for each job title
# for job_title, candidates in shortlisted_threshold.items():
#     print(f"{job_title}: {', '.join(candidates)}")
shortlisted_threshold

# Function to shortlist top N candidates for each job title
def shortlist_candidates_by_number(match_scores_df, num_candidates):
    shortlisted_candidates = {}

    # Loop through each job title (row)
    for job_title in match_scores_df.index:
        # Get the top N CVs with the highest similarity scores for this job title
        top_candidates = match_scores_df.loc[job_title].sort_values(ascending=False).head(num_candidates).index.tolist()
        shortlisted_candidates[job_title] = top_candidates

    return shortlisted_candidates

# Get the shortlisted candidates
shortlisted = shortlist_candidates_by_number(match_scores, cutoff_number)