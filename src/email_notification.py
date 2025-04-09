import smtplib
import ssl
from email.message import EmailMessage
import email_extraction as ee
import candidate_shortlisting as cs

# Sender and receiver email addresses
email_sender = 'karthiksamala33@gmail.com'  # Replace with your email address
email_password = 'jgcmdplcdzqgosnx'  # Replace with your email password (or App Password if 2FA enabled)
email_receiver = 'ksamala1802@gmail.com'  # Replace with the recipient's email address

# Add SSL (layer of security)
context = ssl.create_default_context()

def send_email_to_shortlisted_candidates(shortlisted_candidates, job_title, email_df, sender_email, sender_password):
  try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
      smtp.login(email_sender, email_password)

    # Email content template
      subject = f"Congratulations! You are shortlisted for {job_title}"
      body = f"Dear Candidate,\n\nWe are pleased to inform you that you have been shortlisted for the role of {job_title}. We will contact you soon for the next steps.\n\nBest Regards,\nThe Hiring Team"
      
      body = f"""

            Dear [Candidate's Name],

            Congratulations! You've been shortlisted for the {job_title} role at Accenture. The interview will be scheduled in the coming days, and we'll share further details soon.

            Please feel free to prepare, and let us know if you have any questions.

            Best regards,
            Team Octopus
            HR Team
            Accenture

            """


      for candidate in shortlisted_candidates:
        # Find the email address for this candidate (CV filename) from email_df
        candidate_email = email_df[email_df['CV Filename'] == candidate]['Email'].values[0]

        # Create the email message
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = candidate_email
        em['Subject'] = subject
        em.set_content(body)

        # Send the email
        smtp.sendmail(sender_email, candidate_email, em.as_string())
      
      print(f"Emails sent successfully to shortlisted candidates for {job_title}.")
  except Exception as e:
    print(f"Error sending email: {e}")

for job_title, candidates in cs.shortlisted.items():
    if candidates:  # If there are any shortlisted candidates for this job title
        send_email_to_shortlisted_candidates(candidates, job_title, ee.email_df, email_sender, email_password)


