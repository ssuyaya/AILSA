def file_reading(email_folder):
    """
    Read all files with names prefixed as 'email_xxx.txt' in the specified email folder.
    Each file contains the main text content of the email and optional attachments listed as paths within the file.

    Args:
        email_folder (str): Directory path where the email files are stored.

    Returns:
        list: A list of tuples where each tuple contains the email file name and its content.
    """
    import os

    email_files_content = []

    # Iterate through each file in the email folder
    for root, _, files in os.walk(email_folder):
        for file in files:
            if file.startswith('email_') and file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    email_files_content.append((file, content))

    return email_files_content