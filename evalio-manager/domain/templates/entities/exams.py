from pydantic import BaseModel
from datetime import datetime
from pytz import timezone

class Exam(BaseModel):
    group_id: str
    created_at: datetime = datetime.now(timezone('America/Bogota'))
    student_identification: int
    student_name: str
    exam_path: str
    template_id: str
    period: str = ""
    status: str
    group_name: str = ""
