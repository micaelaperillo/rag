from pydantic import BaseModel
from typing import List

class Recommendation(BaseModel):
    video_id: str
    video_title: str
    video_date: str
    video_duration: str
    playlist_id: str
    playlist_name: str
    source: str
    reason: str
    level: str

class RecommendationList(BaseModel):
    recommendations: List[Recommendation]