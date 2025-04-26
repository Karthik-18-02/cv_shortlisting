import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    # Open the provided PDF
    doc = fitz.open(pdf_path)
    text = ""
    
    # Iterate through all the pages and extract text
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")  # Extracting text from the page
    
    return text

def extract_email(text):
    # This is a basic email extractor using regex
    import re
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None
