import re

def preprocess_data(job_description):
    # Simple preprocessing: remove special characters, make lowercase, etc.
    job_description = re.sub(r'[^a-zA-Z0-9\s]', '', job_description)
    job_description = job_description.lower()
    return job_description
