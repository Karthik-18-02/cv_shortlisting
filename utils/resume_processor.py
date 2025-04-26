import fitz
import spacy
import re
import pandas as pd

nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF resume"""
    document = fitz.open(pdf_path)
    return ''.join(page.get_text() for page in document)

def extract_candidate_info(text):
    """Extract skills and qualifications from resume text"""
    doc = nlp(text)
    return {
        'skills': list(set(ent.text for ent in doc.ents if ent.label_ in ["ORG", "GPE", "TECH"])),
        'qualifications': list(set(sent.text for sent in doc.sents if any(token.text.lower() in ['bachelor', 'master', 'phd', 'diploma', 'certification'] for token in sent)))
    }

def process_job_descriptions(csv_path):
    """Process job descriptions from CSV file"""
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')
    df = df.iloc[:, :2]
    df['Cleaned Description'] = df['Job Description'].str.replace(r'^( Description:|Description:|Job Description:)\s*', '', regex=True)
    return df[['Job Title', 'Cleaned Description']].to_dict('records')