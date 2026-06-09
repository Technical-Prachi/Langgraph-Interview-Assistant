from typing import TypedDict, List


class InterviewState(TypedDict):

    role: str

    current_q: int
    max_q: int

    difficulty: str

    question: str
    answer: str

    score: str
    feedback: str
    improvement: str

    history: List[dict]