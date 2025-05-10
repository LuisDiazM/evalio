from typing import List
from pydantic import BaseModel
from datetime import datetime
import pytz


class Question(BaseModel):
    question: int
    answer: str


class TemplateResponses(BaseModel):
    id: str = ""
    professor_id: str
    created_at: datetime = datetime.now(pytz.timezone("America/Bogota"))
    questions: List[Question]
    subject_name: str
    period: str
    number: int