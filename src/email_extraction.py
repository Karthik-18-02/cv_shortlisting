import os
import re
import pandas as pd
import fitz  # PyMuPDF (for PDF extraction)
import data_preprocessing as dp

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    full_text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        full_text += page.get_text()
    return full_text

# Function to extract email address from the text
def extract_email(text):
    # Regular expression to match email addresses
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_regex, text)
    if match:
        return match.group(0)  # Return the first matched email
    return None

# Function to process all the CVs in the folder and extract emails
def extract_emails_from_cvs(pdf_folder):
    data = []  # List to store CV filename and email

    # Loop through all files in the directory
    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            
            # Extract text from the CV PDF
            extracted_text = extract_text_from_pdf(pdf_path)
            
            # Extract email address from the extracted text
            email = extract_email(extracted_text)
            
            if email:  # If an email is found, add to the data
                data.append({"CV Filename": filename, "Email": email})

    # Create a DataFrame from the extracted data
    email_df = pd.DataFrame(data)
    return email_df

# Example usage
pdf_folder = 'data/CVs1'  # Replace with the path to your CVs folder
email_df = extract_emails_from_cvs(pdf_folder)

# Display the DataFrame with CV filenames and their corresponding emails
print(email_df)

email_dict = email_df.to_dict(orient='records')

# Display the email dictionary
email_dict

