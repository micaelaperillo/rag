from fastapi import FastAPI
from pydantic import BaseModel

from core.recommender import Recommender

app = FastAPI()

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