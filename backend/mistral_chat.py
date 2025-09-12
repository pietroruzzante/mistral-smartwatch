from mistralai import Mistral
from dotenv import load_dotenv
import os
from mistralai.client import MistralClient


class MistralChat:
    def __init__(self, api_key, model, agp_metrics):
        self.client = Mistral(api_key=api_key)
        self.model = model
        self.agp_metrics = agp_metrics
        self.messages = []
        self.start_chat()

    def start_chat(self):
        analysis_prompt = f"""
        You are a helpful assistant for diabetes management. 
        
        You have to analyze this data {self.agp_metrics}
        
        Give an interpretation about the blood glucose state of this diabetics patient. 
        """

        agp_analysis = self.new_message(analysis_prompt)
        self.messages.append({"role":"assistant", "content": agp_analysis})

        print(agp_analysis.choices[0].message.content)

    def new_message(self, new_message):
        self.messages.append({"role": "user", "content": new_message})

        self.client.chat.complete(
            model=self.model,
            messages=self.messages,
        )
        return self.messages[-1]

