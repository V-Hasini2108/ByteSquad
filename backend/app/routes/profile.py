from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import LearnerProfile
from ..schemas import (
    LearnerProfileCreate,
    LearnerProfileResponse
)

router = APIRouter(
    prefix="/api/profile",
    tags=["Profile"]
)


@router.post(
    "",
    response_model=LearnerProfileResponse
)
def create_profile(
    profile: LearnerProfileCreate,
    db: Session = Depends(get_db)
):
    new_profile = LearnerProfile(
        goal=profile.goal,
        skill_level=profile.skillLevel,
        skills=profile.skills,
        study_hours=profile.studyHours,
        duration=profile.duration
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return {
        "id": new_profile.id,
        "goal": new_profile.goal,
        "skillLevel": new_profile.skill_level,
        "skills": new_profile.skills,
        "studyHours": new_profile.study_hours,
        "duration": new_profile.duration
    }