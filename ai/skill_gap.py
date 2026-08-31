import json


def find_missing_skills(required_skills, current_skills):

    required = set(required_skills)
    current = set(current_skills)

    missing = required - current

    return list(missing)


# Load career knowledge base
with open("data/career_paths.json", "r") as file:
    careers = json.load(file)


# Get user's career
career = input("Enter your career goal: ")


# Check whether career exists
if career in careers:

    required_skills = careers[career]

    print("\nRequired Skills:")
    for skill in required_skills:
        print("-", skill)

    # Get user's current skills
    current_input = input(
        "\nEnter your current skills separated by commas: "
    )

    current_skills = [
        skill.strip()
        for skill in current_input.split(",")
    ]

    # Find missing skills
    missing = find_missing_skills(
        required_skills,
        current_skills
    )

    print("\nMissing Skills:")

    for skill in missing:
        print("-", skill)

else:

    print("\nSorry, this career is not available.")