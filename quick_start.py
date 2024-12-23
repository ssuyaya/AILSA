from oscopilot import FridayAgent
from oscopilot import ToolManager
from oscopilot import FridayExecutor, FridayPlanner, FridayRetriever
from oscopilot.utils import setup_config, setup_pre_run
from volcenginesdkarkruntime import Ark

args = setup_config()
#if not args.query:
    #args.query = "Copy any text file located in the /Users/suya/Desktop/oscopilot/working_dir/document directory that contains the word 'agent' to a new folder named 'agents' "
#args.query = "Create a new folder named 'test_friday'"

#args.query = "_SYSTEM_EMAIL_CLASSIFY_PROMPT:You are an expert email categorizing AI model that can understand and classify the user's emails based on their intentions and preferences.\n I will provide you with details about the user, including their persona, preferences, and what they value in emails, along with a dictionary mapping labels to their descriptions or use cases. Based on this information, you need to classify a given email and return an appropriate label and reason.\n Please analyze the user's information and the label the label mapping to determine the most suitable category for the email content provided. If you find an appropriate label, return it along with a concise reason for the classification. If no label is suitable, provide an empty string instead.You should only respond with the format as described below:\n 1. First, understand the user's preferences and the purpose of each label in the mapping.\n 2. Read the email content thoroughly and assess it against the user's criteria and label descriptions.\n 3. Determine the most appropriate label for the email and provide a reason for your classification.\n 4. Output Format: Your final output should be a JSON object containing the label and the reason, structured as follows:\nlabel: <one of the labels specified in the label_mapping> ,reason: <why the given email was classified as the label category>And you should also follow the following criteria:1. Ensure that the label you choose aligns with the user's intentions and the provided label descriptions.2. If no suitable label is found, be sure to return an empty string for the label, rather than forcing an unsuitable label.Now you will be provided with the following information for evaluation:''','_USER_EMAIL_CLASSIFY_PROMPT': '''User's information and email content are as follows:User Information: I am a Software Engineering Student and I am right now on the lookout for work opportunities and advancing my career.I want my mails to be focused on that goal and streamlined, I really don't want to see spammy promotional mails.   Label Mapping: Job: any work related email should go here,Personal: any personal communication from friends or family,Trashy: All Promotional Emails and Spam,Bills: All invoices or finance related things,Email Content:'We at the Music Society are very chill and youll have a lot of freedom to plan and organize any music-related activities you want :3 And your fellow executive members may become your bandmates! Even if youre not very proficient in music - no worries, you can still join us!'. Please classify the email content and tell me label and reasons above." 

#args.query = "Copy any text file located in the /Users/suya/Desktop/oscopilot/working_dir/document directory that contains the word 'agent' to a new folder named 'agents'and tell me the tools you used."

#args.query = "You need to perform some tasks related to classifying emails. \n I have some e-mail content in txt format. \n Your task is: read working_dir/emails/email_001.txt and classify the emails with labels. \n Give the classified labels and the reason for the classification. \n You should complete the task and save the results directly in working_dir/output."

#args.query = "You need to perform some tasks related to classifying emails. \n I have some e-mail content in txt format. \n Your task: categorize the working_dir/emails/email_001.txt content with labels. \n Give the classified labels and the reason for the classification. \n You should complete the task and save the results directly in working_dir/output."

#args.query = "You need to perform some tasks related to classifying emails. \n There's an email now: The Music Society, A.A.H.K.U. is now recruiting new executive members! If you want to find bandmates and meet new friends, then you If you want to find bandmates and meet new friends, then you 're at the right place :D We at the Music Society are very chill and you'll have a lot of freedom to plan and organize any music-related activities you want :3 And your Even if you're not very proficient in music - no worries, you can still join us! If you're interested in becoming a Music Society executive member, you can fill out the form below on or before 27 Nov!\n Your task: categorize the contents of an email with labels. \n Give the classified labels and the reasons for the classification. \n You should complete the task and save the results directly in working_dir/output."

#args.query = "You need to perform some tasks related to classifying emails. \n Emails contents are stored in the directory working_dir/emails \n Your task: Classify email content using labels. Give the classification label and the reason for the classification. \n You should complete the task and save the result directly in working_dir/output."

##args.query = "You need to perform some tasks related to classifying emails. \n Emails contents are stored in the directory working_dir/emails \n Your task: Label them appropriately based on the content of the email. Give the classification label and the reason for the classification. \n You should complete the task and save the result directly in working_dir/output."

#args.query = "I'm so upset, please knock the wooden fish for me 20 times."

args.query = "I'm so anxious, please say something to relieve my anxiety."

task = setup_pre_run(args)
agent = FridayAgent(FridayPlanner, FridayRetriever, FridayExecutor, ToolManager, config=args)
agent.run(task=task)
