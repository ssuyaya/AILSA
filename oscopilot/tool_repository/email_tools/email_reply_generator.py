import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from openai import OpenAI


# Initialize OpenAI client using API key loaded from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Email settings
SENDER_EMAIL = "nananansy0502@gmail.com"  
SENDER_PASSWORD = "mkeinggciyyyeviq"  
SMTP_SERVER = "smtp.gmail.com"  # Email server (Gmail in this case)
SMTP_PORT = 587  # Gmail SMTP port

def process_and_send_files_to_chatgpt():
    """Process all email files in subdirectories, send their content to ChatGPT, and reply back to the sender."""
    email_folder = '/Users/nasiyuan/Desktop/OS-Copilot/emails'  # Root folder where emails are stored
    
    # Check if the directory exists
    if not os.path.exists(email_folder):
        print(f"Directory {email_folder} does not exist.")
        return

    # Walk through the directory to find all email folders (e.g., 'email001', 'email002', ...)
    email_folders = [os.path.join(email_folder, f) for f in os.listdir(email_folder) if os.path.isdir(os.path.join(email_folder, f))]

    if not email_folders:
        print(f"No email folders found in {email_folder}.")
        return

    # Process each email folder
    for folder in email_folders:
        email_file_path = os.path.join(folder, "email.txt")  # Assuming the email content is stored in 'email.txt'
        
        if not os.path.exists(email_file_path):
            print(f"No email.txt found in {folder}. Skipping.")
            continue
        
        # Read the email content
        with open(email_file_path, 'r', encoding='utf-8') as file:
            email_content = file.read()

        # Extract the recipient's email address from the email content
        recipient_email = extract_email_from_content(email_content)
        
        if recipient_email:
            # Send the email content to ChatGPT and generate a reply
            reply_subject, reply_body = generate_reply(email_content)
            
            # Print the generated reply for debugging
            print(f"Generated reply for {folder}:\n{reply_subject}\nContent:\n{reply_body}\n")

            # Send the reply email
            send_reply_email(recipient_email, reply_subject, reply_body)
        else:
            print(f"Failed to extract email address from the content in {folder}. Skipping.")

def generate_reply(email_content, context=""):
    """Generate an email reply using GPT"""
    # Set the system message, telling GPT it is an auto-reply agent
    system_message = """
    You are an automated email assistant designed to provide professional and thoughtful email replies. Your task is to read email content stored in a folder and draft a thoughtful reply.
        Generate a reply to the sender, ensuring:
            - The reply is clear, polite, and addresses the sender's concerns or questions.
            - Any follow-up actions or requests for additional information are included where necessary.
            - Use placeholders for unknown information (e.g., `[Your Name]`, `[Specific Date]`).
        Output the reply in this format:
            - **To:** `<sender's email>` (Extracted from the context of the original email.)
            - **Subject:** `Re: <original email subject>` (Use the subject line if it's available, or leave as `[Subject Not Provided]`.)
            - **Body:** Your well-structured reply to the sender.
        Send the reply back to the sender use my email:
            - **To:** `<sender's email>` (Extracted from the context of the original email.)
            - **Subject:** `Re: <original email subject>` (Use the subject line if it's available, or leave as `[Subject Not Provided]`.)
            - **Body:** Your well-structured reply to the sender.
    """
    if context:
        system_message += "\n\nContext: " + context
    
    # Call OpenAI API to generate the reply
    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME", "gpt-3.5-turbo"),
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": email_content}
        ]
    )

    # Get the generated reply content
    reply_content = response.choices[0].message.content

    # Assume the first line is the subject, the rest is the body
    lines = reply_content.split('\n', 1)
    subject = lines[0].strip()
    body = lines[1].strip() if len(lines) > 1 else ""

    return subject, body

def extract_email_from_content(email_content):
    """Extract the email address from the content"""
    # Use a regular expression to extract the email address from the "From" field
    match = re.search(r"From:.*<(.+?)>", email_content)
    if match:
        return match.group(1)
    else:
        print("Failed to extract email address from the email.")
        return None

def send_reply_email(recipient_email, reply_subject, reply_body):
    """Send the generated reply email"""
    # Create the email object
    msg = MIMEMultipart()
    
    # Fill in the recipient and subject fields
    msg['To'] = recipient_email  # Recipient's email address
    msg['Subject'] = reply_subject  # Use the generated subject
    msg.attach(MIMEText(reply_body, 'plain'))  # Attach the reply body as text

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Start TLS encryption
            server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Log in to the email account
            text = msg.as_string()  # Convert the email to a string
            server.sendmail(SENDER_EMAIL, recipient_email, text)  # Send the email
            print(f"Email successfully sent to {recipient_email}")
    except Exception as e:
        print(f"Error occurred while sending email: {e}")

if __name__ == "__main__":
    # First, fetch the emails using the main function
    # Then, process the emails from the 'emails/' folder and send responses
    process_and_send_files_to_chatgpt()