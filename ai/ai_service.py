import os
from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)


# ---------------------------------------
# Understand user's career goal
# ---------------------------------------

def understand_goal(user_goal, available_careers):

    careers_text = ", ".join(available_careers)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
        You are a career classification assistant.

        Available careers:
        {careers_text}

        User's goal:
        {user_goal}

        Choose the most suitable career from the available careers.

        Return only the career name.
        """
    )

    return response.text.strip()


# ---------------------------------------
# Generate explanation for a recommendation
# ---------------------------------------

def explain_recommendation(skill, prerequisites):

    if prerequisites:

        prerequisite_text = ", ".join(prerequisites)

        return (
            f"{skill} is recommended because it builds on "
            f"{prerequisite_text}."
        )

    return (
        f"{skill} is recommended as a foundation for "
        f"your learning path."
    )
    

    return response.text.strip()