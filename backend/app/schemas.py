from pydantic import BaseModel


class LearnerProfileCreate(BaseModel):
    goal: str
    skillLevel: str
    skills: str
    studyHours: int
    duration: str


class LearnerProfileResponse(BaseModel):
    id: int
    goal: str
    skillLevel: str
    skills: str
    studyHours: int
    duration: str

    class Config:
        from_attributes = True

class RoadmapRequest(BaseModel):
    learnerId: int
    career: str
    currentSkills: list[str]