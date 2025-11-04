from abc import ABC, abstractmethod
from typing import List

from domain.templates.entities.exams import Exam


class IExamRepository(ABC):
    @abstractmethod
    def create_exam(self, exam: Exam) -> str | None:
        pass

    @abstractmethod
    def get_exams_by_template(self, template_id: str) -> List[Exam]:
        pass

    @abstractmethod
    def delete_exams_by_template(self, template_id: str):
        pass

    @abstractmethod
    def delete_exams_by_group(self, group_id: str):
        pass