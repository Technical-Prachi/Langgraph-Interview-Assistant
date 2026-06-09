import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

QUESTION_BANK = {

    "Backend Developer": {
        "easy": [
            "What is REST API?"
        ],
        "medium": [
            "What is JWT?"
        ],
        "hard": [
            "Explain Dependency Injection."
        ]
    },

    "Frontend Developer": {
        "easy": [
            "What is React?"
        ],
        "medium": [
            "What is Virtual DOM?"
        ],
        "hard": [
            "Explain useEffect lifecycle."
        ]
    },

    "Python Developer": {
        "easy": [
            "What is a decorator in Python?"
        ],
        "medium": [
            "Difference between List and Tuple?"
        ],
        "hard": [
            "What is a generator?"
        ]
    }
}


# -------------------------
# Normalize Role
# -------------------------

def normalize_role(role: str):

    role = role.strip().lower()

    if "python" in role:
        return "Python Developer"

    elif "front" in role:
        return "Frontend Developer"

    elif "back" in role:
        return "Backend Developer"

    return "Backend Developer"


# -------------------------
# Generate Question
# -------------------------

def generate_question(role, current_q):

    role = normalize_role(role)

    difficulty_map = {
        0: "easy",
        1: "medium",
        2: "hard"
    }

    difficulty = difficulty_map.get(current_q, "easy")

    questions = QUESTION_BANK[role][difficulty]

    # rotate based on session progress
    index = current_q % len(questions)

    return questions[index]

# -------------------------
# Difficulty Router
# -------------------------

def decide_difficulty(score):

    try:

        score_num = int(
            score.split("/")[0]
        )

    except:
        score_num = 5

    if score_num >= 8:
        return "hard"

    elif score_num >= 5:
        return "medium"

    return "easy"


# -------------------------
# Gemini Evaluation
# -------------------------

def evaluate(question, answer):

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
You are an expert technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Return ONLY valid JSON.

{{
  "score":"8/10",
  "feedback":"2-3 lines feedback",
  "improvement":"1 line improvement"
}}
"""
        )

        text = response.text.strip()

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        return json.loads(text)

    except Exception as e:

        print("Gemini Error:", e)

        return {
            "score": "5/10",
            "feedback": "Gemini quota exceeded.",
            "improvement": "Try giving more detailed answers."
        }
    
    