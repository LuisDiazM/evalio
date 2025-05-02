from domain.templates.entities.exams import Exam
from domain.templates.repositories.db_examp_repo import IExamRepository
from abc import ABC, abstractmethod
import os
from pathlib import Path
import json
from domain.templates.repositories.db_group_repo import IGroupDbRepo
from domain.templates.repositories.logger_repo import LoggerInterface
from domain.templates.repositories.nats_bus import EventPublisher


class IExamsUsecase(ABC):
    @abstractmethod
    async def create_exam(self, exam_data: dict):
        pass


class ExamsUsecase:

    def __init__(self, exam_repo: IExamRepository, 
                 group_repo: IGroupDbRepo,
                 logger_repo: LoggerInterface,
                 event_publisher:EventPublisher):
        self.exam_repo = exam_repo
        self.group_repo = group_repo
        self.logger_repo = logger_repo
        self.event_publisher = event_publisher

    async def create_exam(self, exam_data: dict) -> Exam | None:
        """
        Create an exam in the database.
        :param exam_data: Dictionary containing exam data.
        :return: None
        """
        try:
            exam = self.__make_exam(exam_data)
            if not exam:
                return
            exam_id = self.exam_repo.create_exam(exam=exam)
            if exam_id is None:
                return
            await self.event_publisher.publish(json.dumps({"exam_id": exam_id}))
            return exam
        except Exception as e:
            self.logger_repo.error(f"Error creating exam: {str(e)}")

    def __make_exam(self, exam_data: dict) -> Exam | None:
        try:
            student_id = exam_data.get("student_identification")
            template_id = exam_data.get("template_id")
            group_id = exam_data.get("group_id")
            student_name = exam_data.get("student_name")
            file_location = exam_data.get("exam_path")
            if not all([student_id, template_id, group_id, student_name, file_location]):
                return
            if os.getenv("ENVIRONMENT", "local") == "local":
                localtion = Path(file_location)
                abs_path = os.path.abspath(localtion)
            else:
                # logica para un storage en la nube por ahora solo guarda local
                abs_path = file_location
            group = self.group_repo.get_group_by_id(group_id)
            if group is None:
                return
            return Exam(group_id=group_id,
                        student_identification=int(student_id),
                        status="pending",
                        exam_path=abs_path,
                        template_id=template_id,
                        student_name=student_name,
                        group_name=group.name,
                        period=group.period
                        )
        except Exception as e:
            raise ValueError(f"Error creating exam: {str(e)}")
