import smtplib
import ssl
from email.message import EmailMessage

def send_email(receiver_email, job_title, config):
    msg = EmailMessage()
    msg['Subject'] = f"Shortlisted for {job_title}"
    msg['From'] = config.EMAIL_SENDER
    msg['To'] = receiver_email
    
    body = f"""Dear Candidate,
    
Congratulations! You've been shortlisted for the {job_title} role. 
We'll contact you soon for next steps.

Best regards,
Hiring Team"""
    
    msg.set_content(body)
    
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(config.EMAIL_HOST, config.EMAIL_PORT, context=context) as server:
            server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {e}")