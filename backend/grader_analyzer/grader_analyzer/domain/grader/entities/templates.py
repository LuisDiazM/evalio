from datetime import datetime

import pytz
from pydantic import BaseModel


class Question(BaseModel):
    question: int
    answer: str


class TemplateResponses(BaseModel):
    professor_id: str
    created_at: datetime = datetime.now(pytz.timezone("America/Bogota"))
    questions: list[Question]
    subject_name: str
    period: str
    number: int
