import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "career_paths.json"
)


def load_career_paths():
    """Load career and skill information from the knowledge base."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_skill(skill: str) -> str:
    """Normalize a skill so comparisons are case-insensitive."""

    return skill.strip().lower()


def calculate_skill_gap(
    career: str,
    current_skills: list[str]
):
    """
    Compare learner skills with the required skills
    for the selected career.
    """

    career_paths = load_career_paths()

    if career not in career_paths:
        raise ValueError(f"Career '{career}' not found.")

    required_skills = career_paths[career]["skills"]

    current_normalized = {
        normalize_skill(skill)
        for skill in current_skills
    }

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if normalize_skill(skill) in current_normalized:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    return {
        "career": career,
        "requiredSkills": required_skills,
        "currentSkills": current_skills,
        "matchedSkills": matched_skills,
        "missingSkills": missing_skills
    }