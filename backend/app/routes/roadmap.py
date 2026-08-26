from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Progress
from ..services.recommender import calculate_skill_gap
from ..schemas import RoadmapRequest


router = APIRouter(
    prefix="/api/roadmap",
    tags=["Roadmap"]
)


def generate_roadmap(
    learner_id: int,
    career: str,
    current_skills: list[str],
    db: Session
):
    """Generate a career-specific learning roadmap with progress status."""

    try:
        skill_gap = calculate_skill_gap(
            career,
            current_skills
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    # Get all skills required for the selected career.
    required_skills = skill_gap["requiredSkills"]

    # Get this learner's progress records.
    records = (
        db.query(Progress)
        .filter(
            Progress.learner_id == learner_id
        )
        .all()
    )

    # Store progress using normalized skill names.
    progress_status = {
        record.skill.strip().lower(): record.completed
        for record in records
    }

    # Use the skill order defined in career_paths.json.
    # This makes the roadmap work for every career.
    ordered_skills = required_skills

    roadmap = []

    for index, skill in enumerate(ordered_skills, start=1):

        skill_status = progress_status.get(
            skill.strip().lower()
        )

        if skill_status == 1:
            status = "completed"

        elif skill_status == 0:
            status = "in_progress"

        else:
            status = "not_started"

        roadmap.append({
            "phase": index,
            "skill": skill,
            "status": status,
            "milestone": f"Complete {skill} learning and practice"
        })

    # Calculate completed and remaining skills.
    completed_skills = [
        skill
        for skill in required_skills
        if progress_status.get(
            skill.strip().lower()
        ) == 1
    ]

    remaining_skills = [
        skill
        for skill in required_skills
        if progress_status.get(
            skill.strip().lower()
        ) != 1
    ]

    total_skills = len(required_skills)

    if total_skills > 0:
        progress_percentage = round(
            len(completed_skills)
            / total_skills
            * 100,
            2
        )
    else:
        progress_percentage = 0

    return {
        "learnerId": learner_id,
        "career": career,
        "currentSkills": skill_gap["currentSkills"],
        "matchedSkills": skill_gap["matchedSkills"],
        "totalSkills": total_skills,
        "completedSkills": completed_skills,
        "remainingSkills": remaining_skills,
        "progressPercentage": progress_percentage,
        "roadmap": roadmap
    }


@router.post("")
def create_roadmap(
    request: RoadmapRequest,
    db: Session = Depends(get_db)
):
    return generate_roadmap(
        request.learnerId,
        request.career,
        request.currentSkills,
        db
    )