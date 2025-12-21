from datetime import datetime

import pytz
from pydantic import BaseModel


class Question(BaseModel):
    question: int
    answer: str


class TemplateResponses(BaseModel):
    created_at: datetime = datetime.now(pytz.timezone("America/Bogota"))
    questions: list[Question]
    subject_name: str
    period: str
    number: int
    id: str = ""
    group_id: str = ""
    professor_id: str = ""
