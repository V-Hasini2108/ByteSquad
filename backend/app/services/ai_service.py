from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer("all-MiniLM-L6-v2")
SKILL_DESCRIPTIONS = {
    "OOP": "Object oriented programming concepts including classes, objects, inheritance, polymorphism and encapsulation.",
    
    "Collections": "Java collections such as List, Set, Map and efficient data structure usage.",
    
    "Exception Handling": "Handling errors and exceptions in Java applications.",
    
    "SQL": "SQL queries, relational databases, joins, filtering and database operations.",
    
    "CSS": "Styling web pages using CSS, layouts, responsive design and visual presentation.",
    
    "JavaScript": "JavaScript programming for interactive and dynamic web applications.",
    
    "Git": "Version control using Git, commits, branches and collaborative software development.",
    
    "Spring Boot": "Building Java backend applications using the Spring Boot framework.",
    
    "REST API": "Designing and consuming REST APIs for communication between applications.",
    
    "Database Integration": "Connecting backend applications with databases and performing database operations.",
    
    "Testing": "Software testing, unit testing and verifying application functionality.",
    
    "Project Development": "Building a complete practical software project using multiple development skills."
}
def generate_ai_explanation(
    career: str,
    current_skills: list[str],
    missing_skills: list[str]
):
    """
    Generate a simple personalized explanation
    for the learner's next recommended skill.
    """

    if not missing_skills:
        return {
            "recommendation": "You have completed all identified skills.",
            "reason": "Your current skills match the required skills for this career.",
            "nextAction": "Start a practical project to strengthen your knowledge."
        }

    next_skill = missing_skills[0]

    reasons = {
        "OOP": "OOP is a core foundation for Java application development.",
        "Collections": "Collections are important for storing and processing groups of data in Java.",
        "Exception Handling": "Exception handling helps you build reliable applications.",
        "SQL": "SQL is required for working with relational databases.",
        "CSS": "CSS is necessary for creating well-designed web interfaces.",
        "JavaScript": "JavaScript adds interactivity and dynamic behavior to web applications.",
        "Git": "Git helps you manage source code and collaborate with development teams.",
        "Spring Boot": "Spring Boot is a major framework used for Java backend development.",
        "REST API": "REST APIs allow frontend and backend applications to communicate.",
        "Database Integration": "Database integration connects your backend application to persistent data.",
        "Testing": "Testing helps ensure that your application works correctly.",
        "Project Development": "A practical project helps demonstrate and strengthen your complete skill set."
    }

    reason = reasons.get(
        next_skill,
        f"{next_skill} is one of the skills required for your {career} goal."
    )

    return {
        "recommendation": f"Learn {next_skill} next.",
        "reason": reason,
        "nextAction": f"Start learning {next_skill} and complete a small practice task."
    }
def semantic_recommendation(
    career: str,
    missing_skills: list[str]
):
    if not missing_skills:
        return {
            "skill": None,
            "score": 0,
            "reason": "No skill gaps were identified."
        }

    career_embedding = model.encode([career])

    skill_names = [
        skill for skill in missing_skills
        if skill in SKILL_DESCRIPTIONS
    ]

    skill_descriptions = [
        SKILL_DESCRIPTIONS[skill]
        for skill in skill_names
    ]

    skill_embeddings = model.encode(skill_descriptions)

    similarities = cosine_similarity(
        career_embedding,
        skill_embeddings
    )[0]

    ranked = sorted(
        zip(skill_names, similarities),
        key=lambda item: item[1],
        reverse=True
    )

    best_skill, best_score = ranked[0]

    return {
        "skill": best_skill,
        "score": round(float(best_score), 4),
        "reason": (
            f"{best_skill} has the highest semantic relevance "
            f"to your goal of becoming a {career}."
        )
    }