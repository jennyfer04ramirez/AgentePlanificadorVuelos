import uuid
from typing import Optional


SESSIONS = {}

def get_session(session_id: Optional[str]):
    if session_id and session_id in SESSIONS:
        return session_id, SESSIONS[session_id]

    new_id = str(uuid.uuid4())
    SESSIONS[new_id] = {
        "completed_steps": set(),
        "context": {}
    }
    return new_id, SESSIONS[new_id]


def mark_completed(session_id: str, function_name: str):
    SESSIONS[session_id]["completed_steps"].add(function_name)