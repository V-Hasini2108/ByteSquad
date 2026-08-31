import json


# ---------------------------------------
# Load data
# ---------------------------------------

with open("data/career_paths.json", "r") as file:
    career_data = json.load(file)

with open("data/skills.json", "r") as file:
    skills_data = json.load(file)


# ---------------------------------------
# Find missing skills
# ---------------------------------------

def find_missing_skills(required_skills, current_skills):

    # Convert user's skills to lowercase for comparison
    current_lower = {
        skill.strip().lower()
        for skill in current_skills
    }

    missing = []

    for skill in required_skills:

        if skill.lower() not in current_lower:
            missing.append(skill)

    return missing

# ---------------------------------------
# Get prerequisites
# ---------------------------------------

def get_prerequisites(skill):

    return skills_data.get(skill, {}).get("prerequisites", [])


# ---------------------------------------
# Check if prerequisites are completed
# ---------------------------------------

def can_learn(skill, completed_skills):

    prerequisites = get_prerequisites(skill)

    for prerequisite in prerequisites:

        if prerequisite not in completed_skills:
            return False

    return True


# ---------------------------------------
# Generate roadmap
# ---------------------------------------

def generate_roadmap(missing_skills, completed_skills):

    roadmap = []

    remaining = missing_skills.copy()

    while remaining:

        progress_made = False

        for skill in remaining.copy():

            if can_learn(skill, completed_skills):

                roadmap.append(skill)

                completed_skills.append(skill)

                remaining.remove(skill)

                progress_made = True

                # Add only ONE skill at a time
                break

        if not progress_made:
            break

    return roadmap

# ---------------------------------------
# Main recommendation function
# ---------------------------------------

def recommend_for_career(career, current_skills):

    if career not in career_data:
        return None

    required_skills = career_data[career]

    missing_skills = find_missing_skills(
        required_skills,
        current_skills
    )

    roadmap = generate_roadmap(
        missing_skills,
        current_skills.copy()
    )

    return {
        "career": career,
        "required_skills": required_skills,
        "missing_skills": missing_skills,
        "roadmap": roadmap
    }
if __name__ == "__main__":

    result = recommend_for_career(
        "AI Engineer",
        ["Python"]
    )

    print("\nCareer:")
    print(result["career"])

    print("\nMissing Skills:")
    for skill in result["missing_skills"]:
        print("-", skill)

    print("\nRoadmap:")
    for number, skill in enumerate(result["roadmap"], start=1):
        print(f"{number}. {skill}")