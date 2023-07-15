import os
import openai
from dotenv import load_dotenv

class Assistant():
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = api_key
        self.messages = [
            {"role": "system", "content": ""},
        ]

    def Response(self, user_text):
        self.user_text = user_text

        while True:

            # if user says stop, then breaking the loop
            if self.user_text == "stop":
                break
            
            # storing the user question in the messages list
            self.messages.append({"role": "user", "content": self.user_text})

            # getting the response from OpenAI API
            response= openai.ChatCompletion.create(
                model="gpt-4",
                messages=self.messages,
                temperature=0.3,
                max_tokens=100,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # appending the generated response so that AI remebers past responses
            self.messages.append({"role":"assistant", "content":str(response['choices'][0]['message']['content'])})
            
            # returning the response
            print(response['choices'][0]['message']['content'])
            return response['choices'][0]['message']['content']