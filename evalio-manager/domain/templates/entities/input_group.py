from pydantic import BaseModel

class InputGenTemplate(BaseModel):
    group_id: str
    template_id: str
    date: str = ""