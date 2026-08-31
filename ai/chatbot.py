import os
import json

from dotenv import load_dotenv
from google import genai

from recommendation import recommend_for_career
from ai_service import explain_recommendation


# ==================================================
# 1. Load environment variables
# ==================================================

load_dotenv()


# ==================================================
# 2. Load career data
# ==================================================

with open("data/career_paths.json", "r") as file:
    career_data = json.load(file)


# ==================================================
# 3. Load skill/prerequisite data
# ==================================================

with open("data/skills.json", "r") as file:
    skills_data = json.load(file)


# Get career names from our JSON file
available_careers = list(career_data.keys())


# ==================================================
# 4. Get Gemini API key
# ==================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Gemini API key was not found.")
    exit()


# ==================================================
# 5. Create Gemini client
# ==================================================

client = genai.Client(api_key=api_key)


# ==================================================
# 6. Create Gemini chat
# ==================================================

chat = client.chats.create(
    model="gemini-3.6-flash",
    config={
        "system_instruction": f"""
        You are an AI Learning Path Assistant.

        Available careers in our system:
        {available_careers}

        Your job is to understand the user's career goal.

        Choose only from the available careers.

        Keep responses short and simple.
        Do not invent careers.
        """
    }
)


# ==================================================
# 7. Welcome message
# ==================================================

print("\n======================================")
print("       AI Learning Path Assistant")
print("======================================")

print("Type 'exit' at any time to quit.\n")


# ==================================================
# 8. Get user's career goal
# ==================================================

user_goal = input("What career do you want to pursue? ")


# Allow user to exit
if user_goal.lower().strip() == "exit":
    print("\nGoodbye!")
    exit()


# ==================================================
# 9. Identify career
# ==================================================

career = None


# --------------------------------------------------
# First: check if user directly entered a career
# --------------------------------------------------

for available_career in available_careers:

    if user_goal.strip().lower() == available_career.lower():

        career = available_career
        break


# --------------------------------------------------
# Second: use Gemini for natural-language goals
# --------------------------------------------------

if career is None:

    try:

        response = chat.send_message(
            message=f"""
            The user's career goal is:

            {user_goal}

            Choose the most suitable career from:

            {available_careers}

            Return ONLY the career name.
            """
        )

        career = response.text.strip()

        # Make sure Gemini returned a valid career
        matched_career = None

        for available_career in available_careers:

            if career.lower() == available_career.lower():

                matched_career = available_career
                break

        if matched_career is not None:

            career = matched_career

        else:

            career = None


    except Exception:

        print("\nGemini is currently unavailable.")
        print("Please enter one of the supported careers directly.")

        print("\nAvailable careers:")

        for available_career in available_careers:

            print("-", available_career)

        exit()


# --------------------------------------------------
# If no valid career was found
# --------------------------------------------------

if career is None:

    print("\nSorry, I couldn't identify that career.")

    print("\nAvailable careers:")

    for available_career in available_careers:

        print("-", available_career)

    exit()


print("\nRecommended Career:", career)


# ==================================================
# 10. Get user's current skills
# ==================================================

current_input = input(
    "\nEnter your current skills separated by commas: "
)


# Allow user to exit
if current_input.lower().strip() == "exit":
    print("\nGoodbye!")
    exit()


# Convert input into a list
current_skills = [
    skill.strip()
    for skill in current_input.split(",")
    if skill.strip()
]


# ==================================================
# 11. Generate recommendation
# ==================================================

result = recommend_for_career(
    career,
    current_skills
)


# ==================================================
# 12. Check whether career exists
# ==================================================

if result is None:

    print("\nSorry, this career is not available in our system.")

else:

    # ----------------------------------------------
    # Required skills
    # ----------------------------------------------

    print("\nRequired Skills:")

    for skill in result["required_skills"]:

        print("-", skill)


    # ----------------------------------------------
    # Missing skills
    # ----------------------------------------------

    print("\nMissing Skills:")

    if result["missing_skills"]:

        for skill in result["missing_skills"]:

            print("-", skill)

    else:

        print("None! You already have all required skills.")


    # ----------------------------------------------
    # Personalized roadmap
    # ----------------------------------------------

    print("\n======================================")
    print("       Personalized Learning Path")
    print("======================================")


    if result["roadmap"]:

        for number, skill in enumerate(
            result["roadmap"],
            start=1
        ):

            print(f"\n{number}. {skill}")


            # --------------------------------------
            # Get prerequisites
            # --------------------------------------

            prerequisites = skills_data.get(
                skill,
                {}
            ).get(
                "prerequisites",
                []
            )


            # --------------------------------------
            # Generate explanation
            # --------------------------------------

            explanation = explain_recommendation(
                skill,
                prerequisites
            )


            print("   Why:", explanation)


    else:

        print("\nYou have completed all required skills!")


# ==================================================
# 13. Finish
# ==================================================

print("\nYour roadmap has been generated!")