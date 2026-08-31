from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes import profile, roadmap, progress, recommendations

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PathFinder API",
    description="AI-Powered Personalized Learning Path Recommender",
    version="1.0.0"
)

# Allow the React/Vite frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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