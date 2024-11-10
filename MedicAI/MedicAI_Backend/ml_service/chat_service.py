import os
from dotenv import load_dotenv
import openai
from .prompts import PROMPTS

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class document_information:
    def __init__(self) -> None:
        self.context=None
    
    def insert_context(self,context):
        self.context = context


def Call_OpenAI(message,document_info_class):
    if document_info_class != None:
        body = PROMPTS["Medic_Prompt"].replace("<<Context>>",document_info_class.context).replace("<<Question>>",message)
        
        instruction = PROMPTS["System_Prompt"]

        message = body
        print(message)
    
        response = openai.chat.completions.create(
            model="gpt-4o", #"gpt-3.5-turbo",
            messages=[{"role": "system", "content": instruction},{"role": "user", "content": message}]
        )
    else:
        response = openai.chat.completions.create(
            model="gpt-4o", #"gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )

    # print(response.choices[0].message.content)

    return(response.choices[0].message.content)

import openai

def Call_OpenAISummary(messages_combined, model="gpt-4"):
    # Prepare the prompt for chat summarization
    chat_summary_prompt = PROMPTS["Chat_Summarization_Prompt"].replace("<<Chat Conversation>>", messages_combined)
    
    try:
        # Create a chat completion request
        response = openai.chat.completions.create(
            model=model,  # Use the model you want to use
            messages=[
                {"role": "user", "content": chat_summary_prompt}
            ],
            max_tokens=150,  # Specify max tokens if needed
            temperature=0.7  # Adjust the temperature for variability
        )
        
        # Access the summary from the response
        summary = response.choices[0].message.content
        print(summary)

        return summary  # Return the summary text
    
    except Exception as e:
        print(f"Error during API call: {e}")
        return None  # Handle errors appropriately
