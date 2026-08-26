from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Progress
from ..schemas import RoadmapRequest
from ..services.recommender import calculate_skill_gap
from ..services.ai_service import (
    generate_ai_explanation,
    semantic_recommendation
)


router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"]
)


@router.post("")
def get_recommendations(
    request: RoadmapRequest,
    db: Session = Depends(get_db)
):
    completed_records = (
        db.query(Progress)
        .filter(
            Progress.learner_id == request.learnerId,
            Progress.completed == 1
        )
        .all()
    )

    completed_skills = [
        record.skill
        for record in completed_records
    ]

    actual_skills = list(request.currentSkills)

    for skill in completed_skills:
        if skill.lower() not in {
            existing.lower()
            for existing in actual_skills
        }:
            actual_skills.append(skill)

    try:
        skill_gap = calculate_skill_gap(
            request.career,
            actual_skills
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    missing_skills = skill_gap["missingSkills"]

    if not missing_skills:
        return {
            "career": request.career,
            "currentSkills": actual_skills,
            "completedSkills": completed_skills,
            "skillGaps": [],
            "recommendation": "All roadmap skills completed.",
            "reason": "You have completed all required skills for this career.",
            "nextAction": "Start building a complete project.",
            "mlRecommendation": None,
            "similarityScore": 0,
            "mlReason": "No remaining skills."
        }

    ai_result = generate_ai_explanation(
        career=request.career,
        current_skills=actual_skills,
        missing_skills=missing_skills
    )

    ml_result = semantic_recommendation(
        career=request.career,
        missing_skills=missing_skills
    )

    return {
        "learnerId": request.learnerId,
        "career": request.career,
        "currentSkills": actual_skills,
        "completedSkills": completed_skills,
        "skillGaps": missing_skills,
        "recommendation": ai_result["recommendation"],
        "reason": ai_result["reason"],
        "nextAction": ai_result["nextAction"],
        "mlRecommendation": ml_result["skill"],
        "similarityScore": ml_result["score"],
        "mlReason": ml_result["reason"]
    }