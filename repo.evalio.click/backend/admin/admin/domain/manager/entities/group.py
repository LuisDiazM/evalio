from typing import Dict, List
from pydantic import BaseModel
from datetime import datetime
import pytz


class Student(BaseModel):
    name: str
    identification: int


class Group(BaseModel):
    id: str = ""
    name: str
    period: str
    subject_name: str
    created_at: datetime = datetime.now(pytz.timezone("America/Bogota"))
    professor_id: str
    professor_name: str = ""
    students: List[Student]
