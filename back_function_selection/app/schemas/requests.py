from pydantic import BaseModel
from typing import Optional

class SelectFunctionRequest(BaseModel):
    query: str
    top_k: int = 3
    session_id: Optional[str] = None