from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from graph import ask_question, evaluate_answer
from memory import create_session, sessions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StartInput(BaseModel):
    role: str


class EvalInput(BaseModel):
    session_id: str
    question: str
    answer: str

@app.get("/")
def home():
    return {"status": "running"}
# -------------------------
# START
# -------------------------
@app.post("/start")
def start(data: StartInput):

    session_id = create_session(data.role)
    state = sessions[session_id]

    # ONLY FIRST STEP
    state = ask_question(state)

    sessions[session_id] = state

    return {
        "session_id": session_id,
        "question": state["question"]
    }


# -------------------------
# EVALUATE
# -------------------------
@app.post("/evaluate")
def evaluate_api(data: EvalInput):

    state = sessions[data.session_id]
    state["answer"] = data.answer

    # STEP 1: evaluate only
    state = evaluate_answer(state)

    # STEP 2: next question only if not complete
    if not state["interview_complete"]:
        state = ask_question(state)

    sessions[data.session_id] = state

    return {
        "score": state["score"],
        "feedback": state["feedback"],
        "improvement": state["improvement"],
        "question": state["question"],
        "current_q": state["current_q"],
        "history": state["history"],
        "interview_complete": state["interview_complete"],
        "report": state.get("report")
    }