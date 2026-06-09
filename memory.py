import uuid

# memory.py

sessions = {}

def create_session(role: str):
    import uuid

    session_id = str(uuid.uuid4())

    sessions[session_id] = {
        "role": role,
        "current_q": 0,
        "question": "",
        "answer": "",
        "score": "",
        "feedback": "",
        "improvement": "",
        "history": [],
        "interview_complete": False,
        "report": None
    }

    return session_id


def get_session(session_id):
    return sessions.get(session_id)