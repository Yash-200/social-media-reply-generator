from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class Platform(str, Enum):
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    INSTAGRAM = "instagram"

class ReplyRequest(BaseModel):
    platform: Platform
    post_text: str = Field(..., min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "platform": "twitter",
                "post_text": "Excited to share my new project!"
            }
        }

class ReplyResponse(BaseModel):
    platform: Platform
    post_text: str
    reply: str
    created_at: datetime

class ErrorResponse(BaseModel):
    detail: str 