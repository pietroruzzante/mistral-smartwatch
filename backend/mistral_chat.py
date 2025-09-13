from mistralai import Mistral
from dotenv import load_dotenv
import os
from mistralai.client import MistralClient


class MistralChat:
    def __init__(self, api_key, model):
        self.client = Mistral(api_key=api_key)
        self.model = model
        self.messages = []
        self.messages.append({"role": "system", "content": "You are a helpful diabetes assistant. You always must finish the answer with a question"})


    def new_message(self, new_message):

        self.messages.append({"role": "user", "content": new_message})

        chat_response = self.client.chat.complete(model=self.model, messages=self.messages)
        answer = chat_response.choices[0].message.content

        self.messages.append({"role": "assistant", "content": answer})

        return answer

