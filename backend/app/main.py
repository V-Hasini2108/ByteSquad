from fastapi import FastAPI

from .database import Base, engine
from .routes import profile, roadmap, progress,recommendations

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PathFinder API",
    description="AI-Powered Personalized Learning Path Recommender",
    version="1.0.0"
)

app.include_router(profile.router)
app.include_router(roadmap.router)
app.include_router(progress.router)
app.include_router(recommendations.router)

@app.get("/")
def root():
    return {
        "message": "PathFinder Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }