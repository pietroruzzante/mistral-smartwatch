import pandas as pd
from backend.data_report import report
from backend.mistral_chat import MistralChat
from dotenv import load_dotenv
import os
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]
app = FastAPI()
model = "ministral-8b-latest" # Mistral model
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

    avg_hr = smartwatch_metrics["avg_hr"]
    total_calories = smartwatch_metrics["total_calories"]
    total_steps = smartwatch_metrics["total_steps"]
    avg_stress_level = smartwatch_metrics["avg_stress_level"]

    analysis_prompt = f"""
    You have to analyze my smartwatch's data: 
    Average HR: {avg_hr} bpm,
    Total calories: {total_calories} calories,
    Total steps: {total_steps} steps,
    Average stress level [0-100] {avg_stress_level}

    Give a brief interpretation about my health state during this day.
    """

    answer_interpretation = chat.new_message(analysis_prompt)

    return {"message": answer_interpretation,
            "avg_hr": smartwatch_metrics["avg_hr"],
            "total_steps": smartwatch_metrics["total_steps"],
            "avg_spo2_percentage": smartwatch_metrics["avg_spo2_percentage"],
            "avg_stress_level": smartwatch_metrics["avg_stress_level"],
            "max_stress_level": smartwatch_metrics["max_stress_level"],
            "time_max_stress_level": smartwatch_metrics["time_max_stress_level"],
            "total_calories": smartwatch_metrics["total_calories"],
            "sleep_stage": smartwatch_metrics["sleep_stage"],
            "sleep_count": smartwatch_metrics["sleep_count"],
            }


class ChatMessage(BaseModel):
    message: str

@app.post("/send_message")
def send_message(message: ChatMessage):
    answer = chat.new_message(message.message)
    return {"message": answer}


