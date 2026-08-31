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

    current_lower = {
        skill.strip().lower()
        for skill in current_skills
    }

    missing = []

    for skill in required_skills:

        if skill.strip().lower() not in current_lower:
            missing.append(skill)

    return missing


# ---------------------------------------
# Get prerequisites
# ---------------------------------------

def get_prerequisites(skill):

    skill_info = skills_data.get(skill, {})

    return skill_info.get("prerequisites", [])


# ---------------------------------------
# Check if prerequisite is completed
# ---------------------------------------

def is_skill_completed(skill, completed_skills):

    completed_lower = {
        item.strip().lower()
        for item in completed_skills
    }

    return skill.strip().lower() in completed_lower


# ---------------------------------------
# Check if skill can be learned
# ---------------------------------------

def can_learn(skill, completed_skills):

    prerequisites = get_prerequisites(skill)

    for prerequisite in prerequisites:

        if not is_skill_completed(
            prerequisite,
            completed_skills
        ):
            return False

    return True


# ---------------------------------------
# Generate roadmap
# ---------------------------------------

def generate_roadmap(
    missing_skills,
    completed_skills
):

    roadmap = []

    remaining = missing_skills.copy()

    while remaining:

        progress_made = False

        for skill in remaining.copy():

            if can_learn(
                skill,
                completed_skills
            ):

                roadmap.append(skill)

                completed_skills.append(skill)

                remaining.remove(skill)

                progress_made = True

                # Add one skill at a time
                break

        # Prevent infinite loop
        if not progress_made:
            break

    return roadmap


# ---------------------------------------
# Main recommendation function
# ---------------------------------------

def recommend_for_career(
    career,
    current_skills
):

    # Check whether career exists
    if career not in career_data:
        return None

    career_info = career_data[career]

    # -----------------------------------
    # Get required skills
    # -----------------------------------

    # New format used by teammate
    if isinstance(career_info, dict):

        required_skills = career_info.get(
            "skills",
            []
        )

        description = career_info.get(
            "description",
            ""
        )

    # Backward compatibility
    else:

        required_skills = career_info

        description = ""

    # -----------------------------------
    # Find missing skills
    # -----------------------------------

    missing_skills = find_missing_skills(
        required_skills,
        current_skills
    )

    # -----------------------------------
    # Generate roadmap
    # -----------------------------------

    roadmap = generate_roadmap(
        missing_skills,
        current_skills.copy()
    )

    # -----------------------------------
    # Return result
    # -----------------------------------

    return {
        "career": career,
        "description": description,
        "required_skills": required_skills,
        "missing_skills": missing_skills,
        "roadmap": roadmap
    }


# ---------------------------------------
# Test
# ---------------------------------------

if __name__ == "__main__":

    result = recommend_for_career(
        "Machine Learning Engineer",
        ["Python"]
    )

    if result is None:

        print("Career not found.")

    else:

        print("\nCareer:")
        print(result["career"])

        print("\nDescription:")
        print(result["description"])

        print("\nRequired Skills:")

        for skill in result["required_skills"]:
            print("-", skill)

        print("\nMissing Skills:")

        for skill in result["missing_skills"]:
            print("-", skill)

        print("\nPersonalized Roadmap:")

        for number, skill in enumerate(
            result["roadmap"],
            start=1
        ):
            print(f"{number}. {skill}")