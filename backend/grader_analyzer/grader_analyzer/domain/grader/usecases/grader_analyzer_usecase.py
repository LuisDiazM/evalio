import json
import os
from abc import ABC, abstractmethod

from grader_analyzer.domain.grader.entities.exams import Exam
from grader_analyzer.domain.grader.entities.summary_qualifications import (
    Grade,
    SummaryQualifications,
)
from grader_analyzer.domain.grader.entities.templates import TemplateResponses
from grader_analyzer.domain.grader.repositories.exam_db_repo import IExamRepository
from grader_analyzer.domain.grader.repositories.summary_db_repo import ISumaryRepository
from grader_analyzer.domain.grader.repositories.template_db_repo import (
    ITemplateDBRepository,
)
from grader_analyzer.domain.shared.logger import LoggerInterface
from grader_analyzer.domain.shared.storage_repo import IStorageRepository
from grader_analyzer.domain.shared.utilities.omr import grade_exam
from grader_analyzer.domain.shared.utilities.score_calculator import score_calculator


class IGraderAnalyzerUseCase(ABC):
    @abstractmethod
    def analyze(self, message: str):
        pass


class GraderAnalyzerUsecase(IGraderAnalyzerUseCase):
    def __init__(
        self,
        exam_repo: IExamRepository,
        temp_repo: ITemplateDBRepository,
        summary_repo: ISumaryRepository,
        logger: LoggerInterface,
        storage_repo: IStorageRepository,
    ):
        self.exam_repo = exam_repo
        self.temp_repo = temp_repo
        self.summary_repo = summary_repo
        self.logger = logger
        self.storage_repo = storage_repo

    def analyze(self, message: str):
        exam_id = ""
        exam_path = ""
        vis_output_path = ""
        try:
            self.logger.info(f"message: {message}")
            data = json.loads(message)
            exam_id = data.get("exam_id", "")
            exam = self.exam_repo.get_exam_by_id(exam_id)
            if not exam:
                return
            if exam.status == "completed":
                return

            # Download exam file from storage (MinIO or GCP)
            exam_path = self.__download(exam.exam_path)
            if not exam_path:
                return

            # Prepare output path for visualization
            temp_dir = "outputs/tmp_vis"
            os.makedirs(temp_dir, exist_ok=True)
            vis_output_path = os.path.join(
                temp_dir, f"vis_{exam.student_identification}_{exam.id}.png"
            )

            # Process exam with OMR
            result = grade_exam(exam_path, vis_output_path)
            if len(result.get("responses", [])) == 0:
                self.exam_repo.update_exam(exam.id, {"status": "error"})
                return

            # Get template and calculate score
            template = self.temp_repo.get_template(exam.template_id)
            if not template:
                return
            score = score_calculator(template.questions, result.get("responses", []))

            # Create and save summary
            summary = self.__create_summary(exam, score, template, vis_output_path)
            self.summary_repo.update_summary_qualification(summary)
            self.exam_repo.update_exam(exam.id, {"status": "completed"})
            self.logger.info(
                f"exam {exam_id} student: {exam.student_name} score: {score}"
            )

        except Exception as e:
            self.logger.error(f"error processing {message} --> {str(e)}")
        finally:
            # Always cleanup temporary files after processing
            self.__cleanup_temp_files(exam_path, vis_output_path)

    def __download(self, path: str) -> str:
        """
        Download exam file from storage (MinIO or GCP)
        Always downloads to local temp directory for processing
        :param path: Storage path (blob name or object name)
        :return: Local path of downloaded file
        """
        try:
            # Get bucket name from environment
            if os.getenv("STORAGE_PROVIDER", "gcp").lower() == "minio":
                bucket = os.getenv("MINIO_BUCKET_NAME", "evalio-bucket")
            else:
                bucket = os.getenv("GCP_BUCKET_NAME", "evalio-bucket")

            # Extract filename from path
            filename = os.path.basename(path)
            temp_dir = "outputs/tmp_downloads"
            os.makedirs(temp_dir, exist_ok=True)
            local_path = os.path.join(temp_dir, filename)

            # Download from storage using the configured provider
            downloaded = self.storage_repo.download_file(bucket, path, local_path)
            return downloaded
        except Exception as e:
            self.logger.error(f"Error downloading file {path}: {e}")
            return ""

    def __cleanup_temp_files(self, *file_paths: str):
        """
        Remove temporary files after processing
        :param file_paths: Variable number of file paths to remove
        """
        for file_path in file_paths:
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    self.logger.info(f"Cleaned up temp file: {file_path}")
                except Exception as e:
                    self.logger.error(f"Error removing temp file {file_path}: {e}")

    def __create_summary(
        self,
        exam: Exam,
        score: float,
        template_response: TemplateResponses,
        vis_output_path: str,
    ) -> SummaryQualifications:
        """
        Create summary with student grade and upload visualization to storage
        :param exam: Exam entity with student and template info
        :param score: Calculated grade score
        :param template_response: Template with answer key
        :param vis_output_path: Local path of visualization image to upload
        :return: SummaryQualifications entity with grade details
        """
        # Get bucket name from environment
        bucket = os.getenv("MINIO_BUCKET_NAME") or os.getenv(
            "GCP_BUCKET_NAME", "evalio-bucket"
        )

        # Generate blob name for visualization in storage
        exam_path = exam.exam_path.split("/")
        exam_path = "/".join(exam_path[:-1])
        blob_name = f"{exam_path}/vis_{exam.student_identification}.png"

        # Upload visualization to storage
        self.storage_repo.upload_file(bucket, vis_output_path, blob_name)

        return SummaryQualifications(
            group_id=exam.group_id,
            number=template_response.number,
            template_id=exam.template_id,
            period=exam.period,
            students=[
                Grade(
                    **{
                        "score": score,
                        "student_name": exam.student_name,
                        "student_identification": exam.student_identification,
                        "exam_path": blob_name,
                    }
                )
            ],
        )
