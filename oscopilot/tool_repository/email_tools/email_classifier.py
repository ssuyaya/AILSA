from oscopilot.prompts.friday_pt import prompt
import os
import logging
import json
from oscopilot.prompts.friday_pt import prompt
from oscopilot.utils import self_learning_print_logging, get_project_root_path, save_json
import csv


# Email classification prompts in os
"""
'_SYSTEM_EMAIL_CLASSIFY_PROMPT': '''
You are an expert email categorizing AI model that can understand and classify the user's emails based on their intentions and preferences.

I will provide you with details about the user, including their persona, preferences, and what they value in emails, along with a dictionary mapping labels to their descriptions or use cases. Based on this information, you need to classify a given email and return an appropriate label and reason.

Please analyze the user's information and the label the label mapping to determine the most suitable category for the email content provided. If you find an appropriate label, return it along with a concise reason for the classification. If no label is suitable, provide an empty string instead.

You should only respond with the format as described below:
1. First, understand the user's preferences and the purpose of each label in the mapping.
2. Read the email content thoroughly and assess it against the user's criteria and label descriptions.
3. Determine the most appropriate label for the email and provide a reason for your classification.
4. Output Format: Your final output should be a JSON object containing the label and the reason, structured as follows:
{{
"label": <one of the labels specified in the label_mapping> ,
"reason": <why the given email was classified as the label category>
}}

And you should also follow the following criteria:
1. Ensure that the label you choose aligns with the user's intentions and the provided label descriptions.
2. If no suitable label is found, be sure to return an empty string for the label, rather than forcing an unsuitable label.

Now you will be provided with the following information for evaluation:
''',
'_USER_EMAIL_CLASSIFY_PROMPT': '''
User's information and email content are as follows:
User Information: {user_info}
Label Mapping: {label_mapping}
Email Content: {mail_body}

Please classify the email content into a JSON format as specified above.
'''
"""


class EmailClassifier:
    """
    A class designed to classify emails into predefined categories based on user preferences and email content.
    
    Attributes:
        config (dict): Configuration settings for the email classification process.
        agent (object): An external agent that interacts with the email classification content.
        classifier (object): A classifier object that is responsible for categorizing emails.
        user_info (str): Information about the user's preferences and goals.
        label_mapping (dict): A dictionary mapping labels to their descriptions or use cases.
    """

    def __init__(self, agent, classifier, tool_manager, config):
        super().__init__()
        self.config = config
        self.agent = agent
        #self.classifier = classifier(prompt['_USER_EMAIL_CLASSIFY_PROMPT'], tool_manager)
        self.classifier = classifier(prompt['email_classifier_prompt'], tool_manager)      
  
        self.user_info = """
        I am a Software Engineering Student and I am right now on the lookout for work opportunities and advancing my career.
        I want my mails to be focused on that goal and streamlined, I really don't want to see spammy promotional mails.
        """
        self.label_mapping = {
            "Job": "any work related email should go here",
            "Personal": "any personal communication from friends or family",
            "Trashy": "All Promotional Emails and Spam",
            "Bills": "All invoices or finance related things",
        }

    def _create_prompt(self, email_content):
        """
        Creates a prompt for the email classification task based on user's information and label mapping.

        Args:
            email_content (str): The content of the email to be classified.

        Returns:
            str: A formatted prompt ready for the classification agent.
        """
        return prompt['_USER_EMAIL_CLASSIFY_PROMPT'].format(
            user_info=self.user_info,
            label_mapping=json.dumps(self.label_mapping, indent=4),
            mail_body=email_content
        )

    def classify_email(self, email_content):
        """
        Classifies a single email using the agent based on the provided content.

        Args:
            email_content (str): The content of the email to classify.

        Returns:
            dict: A JSON object containing the classification label and reason.
        """
        prompt_text = self._create_prompt(email_content)
        response = self.agent.run(prompt_text)
        return json.loads(response.strip())

    def process_emails(self, working_directory):
        """
        Processes all .txt email files in the specified directory and classifies them.

        Args:
            working_directory (str): The directory where email files are located.

        Returns:
            None: Saves the classification results in the working directory.
        """
        self_learning_print_logging(self.config)
        emails_directory = os.path.join(working_directory, 'emails')
        results = {}


        # Open the CSV file for writing
        with open(os.path.join(working_directory, 'logs1.csv'), mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            # Write the header to the CSV file
            csv_writer.writerow(['Email Subject', 'Label', 'Reason'])

            for root, _, files in os.walk(emails_directory):
                for file in files:
                    if file.endswith('.txt'):
                        email_path = os.path.join(root, file)
                        try:
                            with open(email_path, 'r', encoding='utf-8') as email_file:
                                email_content = email_file.read()
                                classification = self.classify_email(email_content)
                                logging.info(f"Email '{file}' classified as: {classification}")
                                results[file] = classification

                                # Write the result to the CSV file
                                email_subject = file  # Assuming the file name is the email subject
                                csv_writer.writerow([email_subject, classification.get('label', ''), classification.get('reason', '')])
                        except Exception as e:
                            logging.error(f"Failed to process email '{file}': {str(e)}")

        # Save results to JSON file as before
        save_json(os.path.join(working_directory, 'classification_results.json'), results)
