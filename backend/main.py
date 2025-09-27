import pandas as pd
from backend.data_report import report
from backend.mistral_chat import MistralChat
from dotenv import load_dotenv
import os
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]
app = FastAPI()
model = "mistral-large-latest" # Mistral model

#initializes the chat with Mistral
chat = MistralChat(api_key=api_key, model=model)

@app.get("/")
def read_root():
    return {"message": "Welcome to Mistral AI API!"}

@app.get("/example")
def get_example():
    "Sends example data file to frontend"
    return FileResponse("data/smartwatch_daily_data_example.csv", media_type="text/csv", filename="example.csv")

@app.post("/analyze")
async def analyze(file: UploadFile):
    """
    Uploads the file, starts a new chat, calculate metrics and returns LLM interpretation of data
    """

    data = pd.read_csv(file.file) #reads csv
    smartwatch_metrics = report(data) #calculates metrics using py-agata library

    date = smartwatch_metrics["date"]
    avg_hr = smartwatch_metrics["avg_hr"]
    total_calories = smartwatch_metrics["total_calories"]
    total_steps = smartwatch_metrics["total_steps"]
    avg_stress_level = smartwatch_metrics["avg_stress_level"]

    analysis_prompt = f"""
    You have to analyze my smartwatch's data and return a brief overview of my health quality.
    
    This is my data to analyze:
    date : {date}
    Average HR: {avg_hr} bpm,
    Total calories: {total_calories} calories,
    Total steps: {total_steps} steps,
    Average stress level [0-100] {avg_stress_level}

    Format the output in Markdown with:
    - Title as bold text (e.g. **Health Report for <insert date here with format month day-th year>**)
    - Subtitles as bold text (e.g. **Heart Rate**)
    - Bullets for explanations

    Important: Do not use triple backticks (```) or quotes (''') at the start and do not use # or ## or ### for headings.
    """

    answer_interpretation = chat.new_message(analysis_prompt)

    return {"message": answer_interpretation,
            "avg_hr": smartwatch_metrics["avg_hr"],
            "total_steps": smartwatch_metrics["total_steps"],
            "avg_stress_level": smartwatch_metrics["avg_stress_level"],
            "max_stress_level": smartwatch_metrics["max_stress_level"],
            "total_calories": smartwatch_metrics["total_calories"],
            "sleep_stage": smartwatch_metrics["sleep_stage"],
            "sleep_count": smartwatch_metrics["sleep_count"],
            }


class ChatMessage(BaseModel):
    message: str

@app.post("/send_message")
def send_message(message: ChatMessage):
    "Endpoint for new messages"
    answer = chat.new_message(message.message)
    return {"message": answer}


