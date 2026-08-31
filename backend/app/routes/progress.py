from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Progress
from ..services.recommender import calculate_skill_gap


router = APIRouter(
    prefix="/api/progress",
    tags=["Progress"]
)


@router.get("/{learner_id}")
def get_progress(
    learner_id: int,
    career: str,
    db: Session = Depends(get_db)
):
    try:
        skill_gap = calculate_skill_gap(
            career,
            []
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    required_skills = skill_gap["requiredSkills"]

    records = (
        db.query(Progress)
        .filter(
            Progress.learner_id == learner_id,
            Progress.completed == 1
        )
        .all()
    )

    completed_skills = [
        record.skill
        for record in records
    ]

    completed_normalized = {
        skill.strip().lower()
        for skill in completed_skills
    }

    roadmap_completed = [
        skill
        for skill in required_skills
        if skill.strip().lower() in completed_normalized
    ]

    if required_skills:
        progress_percentage = round(
            len(roadmap_completed)
            / len(required_skills)
            * 100,
            2
        )
    else:
        progress_percentage = 0

    return {
        "learnerId": learner_id,
        "career": career,
        "totalSkills": len(required_skills),
        "completedSkills": roadmap_completed,
        "progressPercentage": progress_percentage
    }


@router.post("/{learner_id}/start")
def start_skill(
    learner_id: int,
    skill: str,
    career: str,
    db: Session = Depends(get_db)
):
    try:
        skill_gap = calculate_skill_gap(
            career,
            []
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    required_skills = skill_gap["requiredSkills"]

    matching_skill = next(
        (
            roadmap_skill
            for roadmap_skill in required_skills
            if roadmap_skill.lower() == skill.strip().lower()
        ),
        None
    )

    if matching_skill is None:
        raise HTTPException(
            status_code=400,
            detail=f"Skill '{skill}' is not part of the {career} roadmap."
        )

    existing = (
        db.query(Progress)
        .filter(
            Progress.learner_id == learner_id,
            Progress.skill == matching_skill
        )
        .first()
    )

    if existing:
        if existing.completed == 1:
            return {
                "learnerId": learner_id,
                "skill": matching_skill,
                "status": "completed"
            }

        return {
            "learnerId": learner_id,
            "skill": matching_skill,
            "status": "in_progress"
        }

    new_progress = Progress(
        learner_id=learner_id,
        skill=matching_skill,
        completed=0
    )

    db.add(new_progress)
    db.commit()

    return {
        "learnerId": learner_id,
        "skill": matching_skill,
        "status": "in_progress"
    }


@router.post("/{learner_id}/complete")
def complete_skill(
    learner_id: int,
    skill: str,
    career: str,
    db: Session = Depends(get_db)
):
    try:
        skill_gap = calculate_skill_gap(
            career,
            []
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    required_skills = skill_gap["requiredSkills"]

    matching_skill = next(
        (
            roadmap_skill
            for roadmap_skill in required_skills
            if roadmap_skill.lower() == skill.strip().lower()
        ),
        None
    )

    if matching_skill is None:
        raise HTTPException(
            status_code=400,
            detail=f"Skill '{skill}' is not part of the {career} roadmap."
        )

    existing = (
        db.query(Progress)
        .filter(
            Progress.learner_id == learner_id,
            Progress.skill == matching_skill
        )
        .first()
    )

    if existing:
        existing.completed = 1
    else:
        new_progress = Progress(
            learner_id=learner_id,
            skill=matching_skill,
            completed=1
        )

        db.add(new_progress)

    db.commit()

    records = (
        db.query(Progress)
        .filter(
            Progress.learner_id == learner_id,
            Progress.completed == 1
        )
        .all()
    )

    completed_skills = [
        record.skill
        for record in records
    ]

    completed_normalized = {
        skill.strip().lower()
        for skill in completed_skills
    }

    roadmap_completed = [
        skill
        for skill in required_skills
        if skill.strip().lower() in completed_normalized
    ]

    if required_skills:
        progress_percentage = round(
            len(roadmap_completed)
            / len(required_skills)
            * 100,
            2
        )
    else:
        progress_percentage = 0

    return {
        "learnerId": learner_id,
        "skill": matching_skill,
        "status": "completed",
        "career": career,
        "totalSkills": len(required_skills),
        "completedSkills": roadmap_completed,
        "progressPercentage": progress_percentage
    }