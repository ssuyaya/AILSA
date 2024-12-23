import os
import imaplib
import email
from email.header import decode_header

class EmailFetcher:
    """
    A tool to fetch emails and save them as .txt files, along with their attachments.
    """
    name = "email_fetcher"
    description = "Fetch the latest emails and save them into folders with their attachments."

    def __init__(self, email_address, password, imap_server="imap.gmail.com"):
        """
        Initialize the EmailFetcher tool.

        Args:
            email_address (str): Email account address.
            password (str): Email account password.
            imap_server (str): IMAP server address (default: Gmail).
        """
        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server
        self.mail = None

    def connect_to_email_server(self):
        """
        Connect to the IMAP email server.
        """
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.email_address, self.password)
            print("Connected to email server successfully.")
        except Exception as e:
            print(f"Failed to connect to email server: {e}")
            self.mail = None

    def fetch_emails(self, max_emails=5, output_folder="working_dir/emails"):
        """
        Fetch the latest emails and save them into dedicated folders.

        Args:
            max_emails (int): Number of latest emails to fetch.
            output_folder (str): Directory to save emails and their attachments.
        """
        if not self.mail:
            print("Not connected to the email server.")
            return

        # Select the inbox
        self.mail.select("inbox")

        # Search for all emails
        status, messages = self.mail.search(None, "ALL")
        if status != "OK":
            print("Failed to retrieve emails.")
            return

        # Get the latest X emails
        mail_ids = messages[0].split()
        latest_email_ids = mail_ids[-max_emails:]

        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Fetch each email
        for i, email_id in enumerate(latest_email_ids):
            status, msg_data = self.mail.fetch(email_id, "(RFC822)")
            if status != "OK":
                print(f"Failed to fetch email with ID: {email_id}")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    self._save_email_with_attachments(msg, i + 1, output_folder)

        print(f"Saved {len(latest_email_ids)} emails to the '{output_folder}' folder.")

    def _save_email_with_attachments(self, msg, email_number, output_folder):
        """
        Save an email and its attachments into a dedicated folder.

        Args:
            msg (email.message.EmailMessage): The email message to save.
            email_number (int): The email number for folder naming.
            output_folder (str): Base directory to save emails and attachments.
        """
        # Decode the email subject
        subject = msg["Subject"]
        if subject:
            subject, encoding = decode_header(subject)[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
        else:
            subject = "No Subject"

        # Decode the sender's email address
        sender = msg.get("From", "Unknown Sender")

        # Create a folder for this email
        email_folder = os.path.join(output_folder, f"email_{email_number:03d}")
        os.makedirs(email_folder, exist_ok=True)

        # Extract email body and attachments
        body = "No plain text content found."
        attachments = []

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    # Get the plain text part of the email
                    body = part.get_payload(decode=True).decode()
                elif "attachment" in content_disposition:
                    # Extract attachment
                    filename = part.get_filename()
                    if filename:
                        filename, encoding = decode_header(filename)[0]
                        if isinstance(filename, bytes):
                            filename = filename.decode(encoding if encoding else "utf-8")
                        attachment_path = os.path.join(email_folder, filename)
                        with open(attachment_path, "wb") as f:
                            f.write(part.get_payload(decode=True))
                        attachments.append(attachment_path)

        # Save the email content into a file
        email_content_file = os.path.join(email_folder, "email.txt")
        with open(email_content_file, "w", encoding="utf-8") as f:
            f.write(f"Subject: {subject}\n")
            f.write(f"From: {sender}\n")
            f.write("\n")
            f.write(body)

        print(f"Saved email content to {email_content_file}")

        # Log saved attachments
        for attachment in attachments:
            print(f"Saved attachment to {attachment}")

    def close_connection(self):
        """
        Close the connection to the email server.
        """
        if self.mail:
            self.mail.logout()
            print("Disconnected from email server.")