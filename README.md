# Smartwatch data analyzer

*A demo application built with **FastAPI**, **Streamlit**, and the **Mistral API** to analyze smartwatch data and provide AI-powered health insights.*

This application demonstrates the possibility of integrating LLMs into digital health and wellness platforms to deliver scalable, personalized feedback from raw data streams.

---

## Features

- Upload smartwatch CSV data or use the built-in **example dataset**  
- Automatic calculation of key health metrics:
  - Heart Rate  
  - Stress Level  
  - Sleep Stages  
  - Physical Activity (steps, calories)  
- AI-powered **Health Report** generated with Mistral models  
- Integrated **Chat Assistant** to ask follow-up questions and receive personalized insights  

## Architecture

The app is organized into two main modules:  

- **Backend (FastAPI)**  
  - Parses smartwatch CSV data  
  - Computes metrics (HR, stress, sleep, calories, steps)  
  - Interacts with Mistral API for natural language analysis  

- **Frontend (Streamlit)**  
  - Provides a clean and interactive UI  
  - Displays metrics and time-series charts  
  - Includes an assistant chat panel for deeper exploration  

## Fast installation

1. Clone the repo:
    ```
    git clone https://github.com/pietroruzzante/mistral-smartwatch.git
    cd mistral-smartwatch
    ```
2. Create a `.env` file with your Mistral API key:
   ```
   MISTRAL_API_KEY=your_api_key_here
   ```
3. Build and run the container
    ```
   docker-compose up --build
    ```
4. Access the app at port 3000: 
    ```
    http://localhost:3000
    ```
5. Click on **`Use example CSV`** button

    The repo includes an example CSV dataset in **data/**.
    You can load it directly from the UI using the "Use example CSV" button.

---

## Loading your CSV

Alternatively, you can upload your own smartwatch data as a CSV file.  
The file must follow this structure:

### Required Columns
- **timestamp** → date and time in the format `YYYY-MM-DD HH:MM`
- **heart_rate_bpm** → heart rate in beats per minute (integer)
- **steps** → number of steps recorded at that timestamp (integer)
- **calories** → calories burned (float or integer)
- **spo2_percent** → blood oxygen saturation in percentage (integer)
- **stress_level** → stress indicator, value between 0–100 (integer)
- **sleep_stage** → categorical label of sleep stage  
  (`Awake`, `Light`, `Deep`, `REM`)

### Example
```csv
timestamp,heart_rate_bpm,steps,calories,spo2_percent,stress_level,sleep_stage
2025-09-14 07:00,80,5,2.5,97,40,Awake
2025-09-14 07:01,82,6,2.6,97,42,Awake
```
---

### Author
Developed by Pietro Ruzzante
AI & Full-Stack Developer