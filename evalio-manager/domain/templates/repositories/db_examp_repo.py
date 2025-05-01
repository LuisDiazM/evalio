from abc import ABC, abstractmethod

from domain.templates.entities.exams import Exam


class IExamRepository(ABC):
    @abstractmethod
    def create_exam(self, exam: Exam) -> str | None:
        pass
