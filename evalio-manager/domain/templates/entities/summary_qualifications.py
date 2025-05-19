from typing import List
from pydantic import BaseModel
from datetime import datetime
from pytz import timezone


class Grade(BaseModel):
    score: float
    student_name: str
    student_identification: int
    exam_path: str


class SummaryQualifications(BaseModel):
    group_id: str
    number: int
    id: str
    period: str
    template_id: str
    created_at: datetime = datetime.now(timezone("America/Bogota"))
    updated_at: datetime = datetime.now(timezone("America/Bogota"))
    students: List[Grade] = []
