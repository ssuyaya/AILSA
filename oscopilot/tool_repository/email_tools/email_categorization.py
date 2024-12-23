import os
import openai
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
    def __init__(self, agent, classifier, tool_manager, config, user_info, label_mapping):
        super().__init__()
        
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
        self.config = config
        self.agent = agent
        
    def classify_email(self, email_content):
        prompt = f"""
        User's information and email content are as follows:
        User Information: {self.user_info}
        Label Mapping: {self.label_mapping}
        Email Content: {email_content}

        Please classify the email content into a JSON format as specified above.
        """
        #response = openai.Completion.create(
        #    engine="text-davinci-003",
        #               prompt=prompt,
        #    max_tokens=150
        #)
        #return response.choices[0].text.strip()

    def process_emails(self, emails_directory, output_directory):
        
        emails_directory = 'working_dir/emails'
        output_directory = 'working_dir/output'
        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)

        for filename in os.listdir(emails_directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(emails_directory, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    email_content = file.read()

                # Classify the email
                classification_result = self.classify_email(email_content)

                # Save the classification result
                output_file_path = os.path.join(output_directory, f"{filename}_classification.txt")
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(classification_result)

# Define user information and label mapping
user_info =  """
        I am a Software Engineering Student and I am right now on the lookout for work opportunities and advancing my career.
        I want my mails to be focused on that goal and streamlined, I really don't want to see spammy promotional mails.
        """
label_mapping = {
            "Job": "any work related email should go here",
            "Personal": "any personal communication from friends or family",
            "Trashy": "All Promotional Emails and Spam",
            "Bills": "All invoices or finance related things",
        }
