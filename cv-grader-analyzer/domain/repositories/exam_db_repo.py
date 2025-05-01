from abc import ABC, abstractmethod

from domain.entities.exams import Exam


class IExamRepository(ABC):
    @abstractmethod
    def get_exam_by_id(self, exam_id: str) -> Exam | None:
        pass

    @abstractmethod
    def update_exam(self, exam_id: str, update_data: dict):
        pass
