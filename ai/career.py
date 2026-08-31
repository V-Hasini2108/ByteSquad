import json

with open("data/career_paths.json", "r") as file:
    careers = json.load(file)


career = input("Enter your career goal: ")

if career in careers:

    required_skills = careers[career]

    print("\nCareer:", career)
    print("Required Skills:")

    for skill in required_skills:
        print("-", skill)

else:
    print("\nSorry, this career is not available.")