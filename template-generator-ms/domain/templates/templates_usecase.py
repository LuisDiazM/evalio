from abc import ABC, abstractmethod
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from domain.templates.entities.input_group import InputGenTemplate
from domain.templates.repositories.db_group_repo import IGroupDbRepo
from domain.templates.utils.template import render_page


class ITemplatesUsecase(ABC):

    @abstractmethod
    def execute(self, input: InputGenTemplate) -> str:
        pass


class TemplateUsecase(ITemplatesUsecase):
    def __init__(self, group_repo: IGroupDbRepo):
        self.group_db = group_repo

    def execute(self, input) -> str:
        try:
            group = self.group_db.get_group(group_name=input.group_name,
                                            professor_id=input.professor_id,
                                            period=input.period)
            group_students = group.students
            students = []
            if len(group_students) == 0:
                return ""
            for student in group_students:
                data = {
                    "name": student.name,
                    "student_id": student.identification,
                    "template_response_id": input.template_id,
                    "group_id": group.name,
                    "subject": group.subject_name,
                    "date": input.date
                }
                students.append(data)
            # Canvas reference to make pdf
            output_path = "temp/responses_sheet.pdf"
            c = canvas.Canvas(output_path, pagesize=letter)
            students_group = [tuple(students[i:i+3])
                            for i in range(0, len(students), 3)]
            for student_group in students_group:
                render_page(c, student_group)
                c.showPage()
            c.save()
            return output_path
        except Exception as e:
            return ""
