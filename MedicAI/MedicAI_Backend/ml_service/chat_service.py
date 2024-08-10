import os
from dotenv import load_dotenv
import openai
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def Call_OpenAI(message):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )

    print(response.choices[0].message.content)

    return(response.choices[0].message.content)