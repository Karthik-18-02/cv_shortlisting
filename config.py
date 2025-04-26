### config.py
import os

class Config:
    # Folder to store uploaded resumes
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
    # Only allow PDF resumes
    ALLOWED_EXTENSIONS = {"pdf"}
    # Path to the job descriptions CSV
    JOB_DESCRIPTIONS_PATH = os.path.join(os.getcwd(), "data", "job_descriptions.csv")
    # Pretrained BERT model name
    BERT_MODEL_NAME = "bert-base-uncased"
    # Score threshold for shortlisting
    THRESHOLD = 0.75

    # Email settings (use env vars for secrets)
    EMAIL_SENDER = os.getenv("EMAIL_SENDER", "karthiksamala33@gmail.com")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "jgcmdplcdzqgosnx")
    EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.example.com")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))