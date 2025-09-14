import pandas as pd
from backend.smartwatch_data_analysis import report
from backend.mistral_chat import MistralChat
from dotenv import load_dotenv
import os
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]
app = FastAPI()
model = "mistral-small-latest" # Mistral model
chat = MistralChat(api_key=api_key, model=model) #initializes the chat with Mistral

@app.get("/")
def read_root():
    return {"message": "Welcome to Mistral AI API!"}

@app.post("/analyze")
async def analyze(file: UploadFile):
    """
    Uploads the file, starts a new chat, calculate metrics and returns LLM interpretation of data
    """

    data = pd.read_csv(file.file) #reads csv
    smartwatch_metrics = report(data) #calculates metrics using py-agata library
    analysis_prompt = f"""
    You have to analyze this data {smartwatch_metrics}

    Give a brief interpretation about the health state of this man during this day.
    """

    answer_interpretation = chat.new_message(analysis_prompt)

    return {"message": answer_interpretation}


class ChatMessage(BaseModel):
    message: str
@app.post("/send_message")
def send_message(message: ChatMessage):
    answer = chat.new_message(message.message)
    return {"message": answer}


