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

        message = PROMPTS["Thought_Process"]+" "+body
    
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