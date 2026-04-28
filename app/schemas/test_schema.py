from pydantic import BaseModel
from typing import Optional

class QuestionBase(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    explanation: Optional[str] = None
    difficulty: str = "medium"
    marks: int = 1

class QuestionResponse(BaseModel):
    id: int
    topic_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty: str
    marks: int

    class Config:
        from_attributes = True

class AnswerSubmit(BaseModel):
    question_id: int
    selected_option: str

class AnswerVerify(BaseModel):
    question_id: int
    selected_option: str

class AnswerResponse(BaseModel):
    is_correct: bool
    correct_option: str
    explanation: Optional[str]
