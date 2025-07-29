from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List
import json
import os

# ----------------------------------------
# App Setup
# ----------------------------------------

app = FastAPI(
    title="Oroma TV API",
    description="API for Oroma TV & QFM Radio application",
    version="1.0.0",
    docs_url="/api/docs" if os.getenv("ENVIRONMENT") == "development" else None,
    redoc_url="/api/redoc" if os.getenv("ENVIRONMENT") == "development" else None
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------
# Pydantic Models
# ----------------------------------------

class AppData(BaseModel):
    app: Dict[str, Any]
    streams: Dict[str, Any]

class Program(BaseModel):
    id: str
    startTime: str
    endTime: str
    title: str
    host: str
    description: str
    imageUrl: str

class DaySchedule(BaseModel):
    id: str
    day: str
    programs: List[Program]

class RadioSchedule(BaseModel):
    days: List[DaySchedule]

# ----------------------------------------
# Load JSON from files
# ----------------------------------------

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

app_data = load_json("data/app_data.json")
radio_schedule = load_json("data/radio_schedule.json")

# ----------------------------------------
# API Routes
# ----------------------------------------

@app.get("/app-data", response_model=AppData)
async def get_app_data():
    return app_data

@app.get("/radio-schedule", response_model=RadioSchedule)
async def get_radio_schedule():
    return radio_schedule

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    return templates.TemplateResponse("privacy_policy.html", {"request": request})
