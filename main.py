from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import os
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Oroma TV API",
    description="API for Oroma TV & QFM Radio application",
    version="1.0.0",
    docs_url="/api/docs" if os.getenv("ENVIRONMENT") == "development" else None,
    redoc_url="/api/redoc" if os.getenv("ENVIRONMENT") == "development" else None
)
# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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

# Your JSON data
app_data = {
    "app": {
        "name": "Oroma TV & QFM Radio",
        "greetings": {
            "morning": "Ibutu Aber 👀",
            "afternoon": "Itye 😊",
            "evening": "Irio aber 😁"
        }
    },
    "streams": {
        "tv": {
            "name": "TV Oroma",
            "description": "Music, News, and Entertainment in Luo",
            "location": "Uganda",
            "streamUrl": "https://mediaserver.oromatv.com/LiveApp/streams/12345.m3u8",
            "share": {
                "message": "Check out this amazing stream on  TV Oroma",
                "url": "https://oromatv.com",
                "title": "Oroma TV Live Stream"
            },
            "about": {
                "title": "Tv Oroma",
                "description": "Northern Uganda's Versetail Tv Station",
                "fullDescription": "Music, News, and Entertainment in Luo. Northern Uganda's Funkiest Radio Station"
            }
        },
        "radio": {
            "name": "QFM Radio",
            "frequency": "94.3",
            "location": "Lira, Uganda",
            "description": "Northern Uganda's Funkiest Radio Station",
            "streamUrl": "https://hoth.alonhosting.com:3975/stream",
            "artworkUrl": "https://assets.mwonya.com/images/artwork/qfm_radio.png"
        }
    }
}

# Radio Schedule
radio_schedule = {
  "days": [
    {
      "id": "1",
      "day": "Monday",
      "programs": [
        { "id": "p1", "startTime": "06:00", "endTime": "06:30", "title": "Morning News", "host": "Sarah Johnson", "description": "QFM Radio Lira", "imageUrl":"https://cdn.pixabay.com/photo/2018/08/27/10/11/radio-cassette-3634616_1280.png" },
        { "id": "p2", "startTime": "06:30", "endTime": "07:00", "title": "Wake Up Mix", "host": "DJ Blake","description": "QFM Radio Lira", "imageUrl":"https://cdn.pixabay.com/photo/2018/08/27/10/11/radio-cassette-3634616_1280.png" },
        { "id": "p3", "startTime": "07:00", "endTime": "07:30", "title": "Traffic Updates", "host": "Mike Peterson","description": "QFM Radio Lira", "imageUrl":"https://cdn.pixabay.com/photo/2018/08/27/10/11/radio-cassette-3634616_1280.png" },
        { "id": "p4", "startTime": "07:30", "endTime": "08:00", "title": "Wake Up Mix", "host": "DJ Blake","description": "QFM Radio Lira", "imageUrl":"https://cdn.pixabay.com/photo/2018/08/27/10/11/radio-cassette-3634616_1280.png" },
        { "id": "p5", "startTime": "08:00", "endTime": "08:30", "title": "Morning Talk", "host": "Rachel & Tom","description": "QFM Radio Lira", "imageUrl":"https://cdn.pixabay.com/photo/2018/08/27/10/11/radio-cassette-3634616_1280.png" },
        { "id": "p6", "startTime": "08:30", "endTime": "09:00", "title": "Morning Talk", "host": "Rachel & Tom","description": "QFM Radio Lira", "imageUrl":"https://cdn.pixabay.com/photo/2018/08/27/10/11/radio-cassette-3634616_1280.png" }
      ]
    },
    {
      "id": "2",
      "day": "Tuesday",
      "programs": [
        { "id": "p49", "startTime": "06:00", "endTime": "06:30", "title": "Morning News", "host": "Sarah Johnson","description": "QFM Radio Lira", "imageUrl":"https://cdn.pixabay.com/photo/2018/08/27/10/11/radio-cassette-3634616_1280.png" },
        { "id": "p51", "startTime": "00:00", "endTime": "00:50", "title": "Jame Up Mix", "host": "DJ Johns","description": "QFM Radio Lira", "imageUrl":"https://cdn.pixabay.com/photo/2018/08/27/10/11/radio-cassette-3634616_1280.png" },
        { "id": "p50", "startTime": "06:30", "endTime": "07:00", "title": "Wake Up Mix", "host": "DJ Blake","description": "QFM Radio Lira", "imageUrl":"https://cdn.pixabay.com/photo/2018/08/27/10/11/radio-cassette-3634616_1280.png" }
      ]
    }
  ]

}

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
    return templates.TemplateResponse(
        "privacy_policy.html",
        {"request": request}
    )