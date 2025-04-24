from pydantic import BaseModel

class InputGenTemplate(BaseModel):
    group_name: str
    period: str
    professor_id: str
    template_id: str
    date: str = ""