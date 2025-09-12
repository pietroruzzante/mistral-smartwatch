import pandas as pd
from sqlalchemy import false

from agp_analysis import agp_analysis
import mistral_chat
from backend.mistral_chat import MistralChat
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]


def main(name):

    new_message = False

    model = "mistral-large-latest"

    data = pd.read_csv('data/' + name + '.csv') #import data
    agp_metrics = agp_analysis(data) #calculate metrics using py-agata library

    MistralChat(api_key=api_key, model=model, agp_metrics=agp_metrics) #initializes the chat with Mistral

    if new_message:
        pass


if __name__ == '__main__':
    main('tr177_ee6ffc')

