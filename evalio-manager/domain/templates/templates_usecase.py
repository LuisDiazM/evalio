from abc import ABC, abstractmethod
from typing import List
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from domain.templates.entities.input_group import InputGenTemplate
from domain.templates.entities.template_responses import Question, TemplateResponses
from domain.templates.repositories.db_examp_repo import IExamRepository
from domain.templates.repositories.db_group_repo import IGroupDbRepo
from domain.templates.repositories.db_template_repo import ITemplateRepository
from domain.templates.repositories.logger_repo import LoggerInterface
from domain.templates.repositories.storage_repo import IStorageRepository
from domain.templates.utils.template import render_page
import os


class ITemplatesUsecase(ABC):

    @abstractmethod
    def generate_template(self, input: InputGenTemplate) -> str:
        pass

    @abstractmethod
    def get_template_by_id(self, template_id: str) -> TemplateResponses | None:
        pass

    @abstractmethod
    def create_template_response(self, template_response: TemplateResponses) -> TemplateResponses | None:
        pass

    @abstractmethod
    def get_templates_by_group(self, group_id: str) -> List[TemplateResponses]:
        pass

    @abstractmethod
    def delete_template(self, template_id: str):
        pass


class TemplateUsecase(ITemplatesUsecase):
    def __init__(self, group_repo: IGroupDbRepo,
                 template_repo: ITemplateRepository,
                 exam_repo: IExamRepository,
                 logger: LoggerInterface,
                 storage_repo: IStorageRepository):
        self.group_db = group_repo
        self.template_db = template_repo
        self.exam_repo = exam_repo
        self.logger = logger
        self.storage_repo = storage_repo

    def generate_template(self, input) -> str:
        try:
            group = self.group_db.get_group_by_id(input.group_id)
            if group is None:
                # self.logger.error(f"group {input.group_id} does not exists" )
                return ""
            group_students = group.students
            students = []
            if len(group_students) == 0:
                raise ValueError(
                    f"group {input.group_id} does not have students")
            for student in group_students:
                data = {
                    "name": student.name,
                    "student_id": student.identification,
                    "template_response_id": input.template_id,
                    "group_id": group.id,
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
                render_page(c, list(student_group))
                c.showPage()
            c.save()
            return output_path
        except Exception as e:
            # self.logger.error(f"error generating template for group {input.group_id}")
            return ""

    def get_template_by_id(self, template_id: str) -> TemplateResponses | None:
        return self.template_db.get_template_by_id(template_id)

    def create_template_response(self, template_response: TemplateResponses) -> TemplateResponses | None:
        template_response.questions = [Question(question=question.question, answer=question.answer.upper())
                                       for question in template_response.questions]
        response = self.template_db.create_template_response(template_response)
        if response != "":
            return template_response
        return

    def get_templates_by_group(self, group_id: str) -> List[TemplateResponses]:
        return self.template_db.get_templates_by_group(group_id)

    def delete_template(self, template_id: str):
        try:
            # Obtener el template para obtener el group_id
            template = self.template_db.get_template_by_id(template_id)
            if template:
                group_id = template.group_id
                # Eliminar carpeta del cloud storage si no estamos en modo local
                if os.getenv("ENVIRONMENT", "local") != "local":
                    folder_path = f"exams/{group_id}/{template_id}/"
                    if self.storage_repo.delete_folder(folder_path):
                        self.logger.info(f"Cloud storage folder deleted: {folder_path}")
                    else:
                        self.logger.warning(f"Failed to delete cloud storage folder: {folder_path}")
                else:
                    self.logger.info("Local environment - skipping cloud storage deletion")
            else:
                self.logger.warning(f"Template not found: {template_id}")
            
            # Eliminar de la base de datos
            self.template_db.delete_template_response(template_id)
            self.exam_repo.delete_exams_by_template(template_id)
        except Exception as e:
            self.logger.error(f"Error deleting template {template_id}: {str(e)}")
            raise
