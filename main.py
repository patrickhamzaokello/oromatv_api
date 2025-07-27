from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import os

app = FastAPI(
    title="Oroma TV API",
    description="API for Oroma TV & QFM Radio application",
    version="1.0.0",
    docs_url="/api/docs" if os.getenv("ENVIRONMENT") == "development" else None,
    redoc_url="/api/redoc" if os.getenv("ENVIRONMENT") == "development" else None
)

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

# Your JSON data
app_data = {
    "app": {
        "name": "Oroma TV & QFM Radio",
        "greetings": {
            "morning": "Good Morning",
            "afternoon": "Good Afternoon",
            "evening": "Good Evening"
        }
    },
    "streams": {
        "tv": {
            "name": "TV Oroma",
            "description": "Music, News, and Entertainment in Luo",
            "location": "Uganda",
            "streamUrl": "https://mediaserver.oromatv.com/LiveApp/streams/12345.m3u8",
            "share": {
                "message": "Check out this amazing stream on Oroma TV!",
                "url": "https://oromatv.com/live",
                "title": "Oroma TV Live Stream"
            },
            "about": {
                "title": "Tv Oroma",
                "description": "Tv me kumalo me Uganda",
                "fullDescription": "Music, News, and Entertainment in Luo"
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

@app.get("/app-data", response_model=AppData)
async def get_app_data():
    return app_data

@app.get("/health")
async def health_check():
    return {"status": "healthy"}