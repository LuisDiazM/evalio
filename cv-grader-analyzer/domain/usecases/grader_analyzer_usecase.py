from abc import ABC, abstractmethod
import os
import json
from domain.entities.exams import Exam
from domain.entities.summary_qualifications import Grade, SummaryQualifications
from domain.entities.templates import TemplateResponses
from domain.repositories.exam_db_repo import IExamRepository
from domain.repositories.logger_repo import LoggerInterface
from domain.repositories.summary_db_repo import ISumaryRepository
from domain.repositories.template_db_repo import ITemplateDBRepository
from domain.usecases.utilities.score_calculator import score_calculator
from domain.usecases.utilities.omr import grade_exam


class IGraderAnalyzerUseCase(ABC):
    @abstractmethod
    def analyze(self, message: str):
        pass


class GraderAnalyzerUsecase(IGraderAnalyzerUseCase):

    def __init__(self, exam_repo: IExamRepository,
                 temp_repo: ITemplateDBRepository,
                 summary_repo: ISumaryRepository,
                 logger:LoggerInterface):
        self.exam_repo = exam_repo
        self.temp_repo = temp_repo
        self.summary_repo = summary_repo
        self.logger = logger

    def analyze(self, message:str):
        try:
            self.logger.info(f"message: {message}")
            data = json.loads(message)
            exam_id = data.get("exam_id")
            exam = self.exam_repo.get_exam_by_id(exam_id)
            if not exam:
                return
            if exam.status == "completed":
                return
            exam_path = self.__download(exam.exam_path)
            if not exam_path:
                return
            result = grade_exam(
                exam_path, f"{exam.student_identification}_{exam.id}")
            if len(result.get("responses"))==0:
                self.exam_repo.update_exam(exam.id, {"status": "error"})
                return
            template = self.temp_repo.get_template(exam.template_id)
            if not template:
                return
            score = score_calculator(template.questions, result.get("responses"))
            summary = self.__create_summary(exam, score, template, result.get("output",""))
            self.summary_repo.update_summary_qualification(summary)
            self.exam_repo.update_exam(exam.id, {"status": "completed"})
            self.logger.info(f"exam {exam_id} student: {exam.student_name} score: {score}")
            os.remove(exam_path)
        except Exception as e:
            self.logger.error(f"error processing {exam_id} --> {str(e)}")

    def __download(self, path) -> str:
        if os.getenv("ENVIRONMENT", "local") == "local":
            if os.path.exists(path):
                return path
        return ""

    def __create_summary(self, exam: Exam, score: float, template_response: TemplateResponses, output:str) -> SummaryQualifications:
        return SummaryQualifications(
            group_id=exam.group_id,
            number=template_response.number,
            id=exam.id,
            period=exam.period,
            students=[Grade(**{
                "score": score,
                "student_name": exam.student_name,
                "student_identification": exam.student_identification,
                "exam_path": output
            })]
        )
