import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_notifications(shortlisted_candidates):
    sender_email = "karthiksamala33@gmail.com"
    sender_password = "jgcmdplcdzqgosnx"
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    
    for job_title, candidates in shortlisted_candidates.items():
        for candidate in candidates:
            receiver_email = candidate[0]  # Candidate email (from extracted info)
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = f"Congratulations! You are shortlisted for {job_title}"
            
            body = f"""

            Dear [Candidate's Name],

            Congratulations! You've been shortlisted for the {job_title} role at Accenture. The interview will be scheduled in the coming days, and we'll share further details soon.

            Please feel free to prepare, and let us know if you have any questions.

            Best regards,
            Team Octopus
            HR Team
            Accenture

            """
            message.attach(MIMEText(body, 'plain'))
            
            server.sendmail(sender_email, receiver_email, message.as_string())
    
    server.quit()
