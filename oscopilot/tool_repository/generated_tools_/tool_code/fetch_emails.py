def fetch_emails(email_address, password, max_emails=5, output_folder="/Users/fanyi/OS-Copilot/working_dir/emails"):
    """
    Fetch the first 5 emails in the mailbox with the specified email address and password, and save them to the specified output folder.

    Args:
        email_address (str): Email account address.
        password (str): Email account password.
        max_emails (int): Number of emails to fetch (default is 5).
        output_folder (str): Directory to save the emails (default is '/Users/fanyi/OS-Copilot/working_dir/emails').

    Returns:
        str: Information message indicating the number of emails saved to the output folder.
    """
    import os
    import imaplib
    import email
    from email.header import decode_header

    class EmailFetcher:
        def __init__(self, email_address, password, imap_server="imap.gmail.com"):
            self.email_address = email_address
            self.password = password
            self.imap_server = imap_server
            self.mail = None

        def connect_to_email_server(self):
            try:
                self.mail = imaplib.IMAP4_SSL(self.imap_server)
                self.mail.login(self.email_address, self.password)
                print("Connected to email server successfully.")
            except Exception as e:
                print(f"Failed to connect to email server: {e}")
                self.mail = None

        def fetch_emails(self, max_emails=5, output_folder="working_dir/emails"):
            if not self.mail:
                print("Not connected to the email server.")
                return

            self.mail.select("inbox")

            status, messages = self.mail.search(None, "ALL")
            if status != "OK":
                print("Failed to retrieve emails.")
                return

            mail_ids = messages[0].split()
            latest_email_ids = mail_ids[-max_emails:]

            os.makedirs(output_folder, exist_ok=True)

            for i, email_id in enumerate(latest_email_ids):
                status, msg_data = self.mail.fetch(email_id, "(RFC822)")
                if status != "OK":
                    print(f"Failed to fetch email with ID: {email_id}")
                    continue

                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        self._save_email_with_attachments(msg, i + 1, output_folder)

            return f"Saved {len(latest_email_ids)} emails to the '{output_folder}' folder."

        def _save_email_with_attachments(self, msg, email_number, output_folder):
            subject = msg["Subject"]
            if subject:
                subject, encoding = decode_header(subject)[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
            else:
                subject = "No Subject"

            sender = msg.get("From", "Unknown Sender")

            email_folder = os.path.join(output_folder, f"email_{email_number:03d}")
            os.makedirs(email_folder, exist_ok=True)

            body = "No plain text content found."
            attachments = []

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition", ""))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode()
                    elif "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            filename, encoding = decode_header(filename)[0]
                            if isinstance(filename, bytes):
                                filename = filename.decode(encoding if encoding else "utf-8")
                            attachment_path = os.path.join(email_folder, filename)
                            with open(attachment_path, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            attachments.append(attachment_path)

            email_content_file = os.path.join(email_folder, "email.txt")
            with open(email_content_file, "w", encoding="utf-8") as f:
                f.write(f"Subject: {subject}\n")
                f.write(f"From: {sender}\n\n")
                f.write(body)

            for attachment in attachments:
                pass

        def close_connection(self):
            if self.mail:
                self.mail.logout()
                print("Disconnected from email server.")

    # Instantiate EmailFetcher and fetch emails
    email_fetcher = EmailFetcher(email_address, password)
    email_fetcher.connect_to_email_server()
    result = email_fetcher.fetch_emails(max_emails, output_folder)
    email_fetcher.close_connection()

    return result