from abc import ABC, abstractmethod
import os
import json
from domain.entities.exams import Exam
from domain.entities.summary_qualifications import Grade, SummaryQualifications
from domain.entities.templates import TemplateResponses
from domain.repositories.exam_db_repo import IExamRepository
from domain.repositories.logger_repo import LoggerInterface
from domain.repositories.storage_repo import IStorageRepository
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
                 logger:LoggerInterface,
                 storage_repo: IStorageRepository):
        self.exam_repo = exam_repo
        self.temp_repo = temp_repo
        self.summary_repo = summary_repo
        self.logger = logger
        self.storage_repo = storage_repo

    def analyze(self, message:str):
        exam_id = ""
        try:
            self.logger.info(f"message: {message}")
            data = json.loads(message)
            exam_id = data.get("exam_id","")
            exam = self.exam_repo.get_exam_by_id(exam_id)
            if not exam:
                return
            if exam.status == "completed":
                return
            exam_path = self.__download(exam.exam_path)
            if not exam_path:
                return
            temp_dir = "outputs/tmp_vis"
            os.makedirs(temp_dir, exist_ok=True)
            vis_output_path = os.path.join(temp_dir, f"vis_{exam.student_identification}_{exam.id}.png")
            result = grade_exam(
                exam_path, vis_output_path)
            if len(result.get("responses",[]))==0:
                self.exam_repo.update_exam(exam.id, {"status": "error"})
                return
            template = self.temp_repo.get_template(exam.template_id)
            if not template:
                return
            score = score_calculator(template.questions, result.get("responses",[]))
            summary = self.__create_summary(exam, score, template, result.get("output",""))
            self.summary_repo.update_summary_qualification(summary)
            self.exam_repo.update_exam(exam.id, {"status": "completed"})
            self.logger.info(f"exam {exam_id} student: {exam.student_name} score: {score}")
            if os.getenv("ENVIRONMENT") == "cloud":
                os.remove(exam_path)
                os.remove(vis_output_path)
        except Exception as e:
            self.logger.error(f"error processing {exam_id} --> {str(e)}")

    def __download(self, path) -> str:
        if os.getenv("ENVIRONMENT", "local") == "local":
            if os.path.exists(path):
                return path
        # Si no es local, descargar desde GCP
        # path esperado: bucket/object_path
        bucket = os.getenv("GCP_BUCKET_NAME","evalio-multimedia-pdn")
        # path puede ser solo el nombre del blob
        filename = os.path.basename(path)
        temp_dir = "outputs/tmp_downloads"
        os.makedirs(temp_dir, exist_ok=True)
        local_path = os.path.join(temp_dir, filename)
        downloaded = self.storage_repo.download_file(bucket, path, local_path)
        return downloaded

    def __create_summary(self, exam: Exam, score: float, template_response: TemplateResponses, output:str) -> SummaryQualifications:
        # Subir la imagen procesada al bucket y guardar el blob name
        bucket = os.getenv("GCP_BUCKET_NAME","evalio-multimedia-pdn")
        exam_path = exam.exam_path.split("/")
        exam_path = "/".join(exam_path[:-1])
        blob_name = f"{exam_path}/vis_{exam.student_identification}.png"
        self.storage_repo.upload_file(bucket, output, blob_name)
        return SummaryQualifications(
            group_id=exam.group_id,
            number=template_response.number,
            template_id=exam.template_id,
            period=exam.period,
            students=[Grade(**{
                "score": score,
                "student_name": exam.student_name,
                "student_identification": exam.student_identification,
                "exam_path": blob_name
            })]
        )
