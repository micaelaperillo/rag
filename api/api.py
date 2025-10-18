from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from core.recommender import Recommender

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendRequest(BaseModel):
    query: str
    user_preferences: str

@app.get("/test")
def test():
    return {"message": "Hello, World!"}

@app.post("/recommend")
def recommend(request: RecommendRequest):
    recommender = Recommender()
    return recommender.recommend(request.query, request.user_preferences)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)