import os
from dotenv import load_dotenv
from google import genai

from recommendation import recommend_for_career


# ---------------------------------------
# 1. Load Gemini API key
# ---------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Gemini API key was not found.")
    exit()


# ---------------------------------------
# 2. Create Gemini client
# ---------------------------------------

client = genai.Client(api_key=api_key)


# ---------------------------------------
# 3. Get user's career goal
# ---------------------------------------

user_goal = input("\nWhat is your career goal? ")


# ---------------------------------------
# 4. Ask Gemini to understand the goal
# ---------------------------------------

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=f"""
    You are a career classification assistant.

    The available careers are:

    AI Engineer
    Data Scientist
    Web Developer

    The user's goal is:

    {user_goal}

    Choose the most suitable career from the available careers.

    Return only the career name.
    """
)


career = response.text.strip()

print("\nGemini identified career:", career)


# ---------------------------------------
# 5. Get user's current skills
# ---------------------------------------

current_input = input(
    "\nEnter your current skills separated by commas: "
)

current_skills = [
    skill.strip()
    for skill in current_input.split(",")
]


# ---------------------------------------
# 6. Call our recommendation engine
# ---------------------------------------

result = recommend_for_career(
    career,
    current_skills
)


# ---------------------------------------
# 7. Display recommendation
# ---------------------------------------

if result is None:

    print("\nSorry, this career is not available in our system.")

else:

    print("\nRequired Skills:")

    for skill in result["required_skills"]:
        print("-", skill)

    print("\nMissing Skills:")

    for skill in result["missing_skills"]:
        print("-", skill)

    print("\nPersonalized Learning Path:")

    for number, skill in enumerate(
        result["roadmap"],
        start=1
    ):
        print(f"{number}. {skill}")