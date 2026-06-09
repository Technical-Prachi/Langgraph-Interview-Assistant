from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, START, END

from agent import generate_question, evaluate


# -------------------------
# STATE
# -------------------------
class InterviewState(TypedDict):
    role: str
    current_q: int

    question: str
    answer: str

    score: str
    feedback: str
    improvement: str

    history: List[dict]

    interview_complete: bool
    report: Optional[dict]


# -------------------------
# NODE 1: ASK QUESTION
# -------------------------
def ask_question(state: InterviewState):

    question = generate_question(
        state["role"],
        state["current_q"]
    )

    state["question"] = question
    state["answer"] = ""

    return state


# -------------------------
# NODE 2: EVALUATE ANSWER
# -------------------------
def evaluate_answer(state: InterviewState):

    result = evaluate(
        state["question"],
        state["answer"]
    )

    state["score"] = result["score"]
    state["feedback"] = result["feedback"]
    state["improvement"] = result["improvement"]

    state["history"].append({
        "question": state["question"],
        "answer": state["answer"],
        "score": state["score"],
        "feedback": state["feedback"],
        "improvement": state["improvement"]
    })

    state["current_q"] += 1

    # -------------------------
    # END LOGIC
    # -------------------------
    if state["current_q"] >= 3:

        state["interview_complete"] = True

        total = 0
        for item in state["history"]:
            total += int(item["score"].split("/")[0])

        avg = round(total / len(state["history"]), 1)

        if avg >= 8:
            strengths = ["Strong communication", "Problem solving"]
            weaknesses = ["Minor edge cases"]
        elif avg >= 5:
            strengths = ["Basic understanding", "Good effort"]
            weaknesses = ["System design", "Deep concepts"]
        else:
            strengths = ["Attempting answers"]
            weaknesses = ["Weak fundamentals"]

        state["report"] = {
            "overall_score": f"{avg}/10",
            "strengths": strengths,
            "weaknesses": weaknesses
        }

    else:
        state["interview_complete"] = False

    return state


# -------------------------
# ROUTER
# -------------------------
def route_next(state: InterviewState):

    if state["interview_complete"]:
        return "end"

    return "ask"


# -------------------------
# BUILD GRAPH
# -------------------------
builder = StateGraph(InterviewState)

builder.add_node("ask", ask_question)
builder.add_node("evaluate", evaluate_answer)

builder.add_edge(START, "ask")
builder.add_edge("ask", "evaluate")

builder.add_conditional_edges(
    "evaluate",
    route_next,
    {
        "ask": "ask",
        "end": END
    }
)

graph = builder.compile()