import json


# Load skills and prerequisites from skills.json
with open("data/skills.json", "r") as file:
    skills_data = json.load(file)


# Function 1: Get prerequisites of a skill
def get_prerequisites(skill):

    return skills_data[skill]["prerequisites"]


# Function 2: Check whether a skill can be learned
def can_learn(skill, completed_skills):

    prerequisites = get_prerequisites(skill)

    for prerequisite in prerequisites:

        if prerequisite not in completed_skills:
            return False

    return True


# Function 3: Find the next skill to learn
def get_next_skill(missing_skills, completed_skills):

    for skill in missing_skills:

        if can_learn(skill, completed_skills):
            return skill

    return None


# Function 4: Generate the complete learning roadmap
def generate_roadmap(missing_skills, completed_skills):

    roadmap = []

    # Make a copy so we don't change the original list
    remaining_skills = missing_skills.copy()

    while remaining_skills:

        next_skill = get_next_skill(
            remaining_skills,
            completed_skills
        )

        # If no skill can be learned,
        # stop to avoid an infinite loop.
        if next_skill is None:
            break

        # Add the skill to the roadmap
        roadmap.append(next_skill)

        # Treat it as completed so later skills can depend on it
        completed_skills.append(next_skill)

        # Remove it from the remaining skills
        remaining_skills.remove(next_skill)

    return roadmap


# Test data
missing_skills = [
    "Mathematics",
    "Statistics",
    "Machine Learning",
    "Deep Learning",
    "AI Project"
]

completed_skills = [
    "Python"
]


# Generate roadmap
roadmap = generate_roadmap(
    missing_skills,
    completed_skills
)


# Display roadmap
print("\nPersonalized Learning Path:")

for number, skill in enumerate(roadmap, start=1):
    print(f"{number}. {skill}")