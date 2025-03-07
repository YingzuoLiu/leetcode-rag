from pydantic import BaseModel
from typing import Dict, Any, Optional

class ProblemRequest(BaseModel):
    problem: str
    language: str = "python"

class SolutionResponse(BaseModel):
    code: str
    reasoning: str
    features: Dict[str, Any]
    solution_id: str

class FeedbackRequest(BaseModel):
    solution_id: str
    is_positive: bool
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: str
    solution_id: str
    success: bool
    message: str