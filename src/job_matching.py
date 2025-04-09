import nlp_processing as np
import data_preprocessing as dp
import fitz  # PyMuPDF

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    full_text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        full_text += page.get_text()
    return full_text

# Example usage with one of the uploaded PDFs
pdf_path = 'C1061.pdf'  # Replace with the path to other PDFs for further extraction
extracted_text = extract_text_from_pdf(pdf_path)

# Print the first 500 characters of the extracted text for review
print(extracted_text)


import spacy

# Load SpaCy model for NER
nlp = spacy.load('en_core_web_sm')

# Example function to extract skills, qualifications, and experience from a CV
def extract_candidate_info(cv_text):
    doc = nlp(cv_text)

    # Extract named entities such as skills and qualifications
    skills = [ent.text for ent in doc.ents if ent.label_ == "ORG" or ent.label_ == "GPE"]  # Assume skills are organization or locations
    qualifications = [ent.text for ent in doc.ents if ent.label_ == "WORK_OF_ART"]  # You can modify for qualifications
    experience = [sent.text for sent in doc.sents if "experience" in sent.text.lower()]  # Simple check for experience-related sentences

    return {"Skills": skills, "Qualifications": qualifications, "Experience": experience}

# Extract candidate information
candidate_info = extract_candidate_info(extracted_text)
print(candidate_info)

from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Function to get BERT embeddings for a text
def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # Use the embeddings of the [CLS] token as the sentence representation
    embeddings = outputs.last_hidden_state[:, 0, :].numpy()
    return embeddings

# Function to calculate match score using BERT embeddings
def calculate_match_score_bert(job_desc, candidate_info):
    # Get BERT embeddings for the job description
    job_desc_embedding = get_bert_embeddings(job_desc)

    # Combine candidate skills and qualifications into a single text
    candidate_skills_qualifications = " ".join(candidate_info["Skills"] + candidate_info["Qualifications"])

    # Get BERT embeddings for the candidate skills and qualifications
    candidate_embedding = get_bert_embeddings(candidate_skills_qualifications)

    # Calculate cosine similarity between job description and candidate's info
    similarity_score = cosine_similarity(job_desc_embedding, candidate_embedding)

    return similarity_score[0][0]  # Return the match score

# # Example usage:
# # Sample job description
# job_desc = "We are looking for a skilled Software Engineer with experience in Python, TensorFlow, and cloud computing."

# # Sample extracted candidate info (from CV text)
# candidate_info = {
#     "Skills": ["Python", "TensorFlow", "Machine Learning", "Cloud Computing"],
#     "Qualifications": ["Ph.D. in Artificial Intelligence", "Master's in Software Engineering"]
# }

# # Calculate match score between job description and candidate
# match_score = calculate_match_score_bert(job_desc, candidate_info)
# print(f"Match Score: {match_score:.4f}")

job_data_df = dp.job_description_df.iloc[:, [0, 3]]
job_data = job_data_df.to_dict(orient='records')