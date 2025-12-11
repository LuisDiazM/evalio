import json
from abc import ABC, abstractmethod

from admin.domain.manager.entities.exams import Exam
from admin.domain.manager.repositories.db_exams_summary_repo import IExamRepository
from admin.domain.manager.repositories.db_group_repo import IGroupDbRepo
from admin.domain.shared.event_repo import EventPublisher
from admin.domain.shared.storage_repo import IStorageRepository


class IExamsUsecase(ABC):
    @abstractmethod
    async def create_exam(self, exam_data: dict):
        pass

    @abstractmethod
    def get_exams_by_template(self, template_id: str) -> list[Exam]:
        pass


class ExamsUsecase:
    def __init__(
        self,
        exam_repo: IExamRepository,
        group_repo: IGroupDbRepo,
        event_publisher: EventPublisher,
        storage_repo: IStorageRepository,
    ):
        self.exam_repo = exam_repo
        self.group_repo = group_repo
        self.event_publisher = event_publisher
        self.storage_repo = storage_repo

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
            await self.event_publisher.publish(data=json.dumps({"exam_id": exam_id}))  # type: ignore
            return exam
        except Exception as e:
            print(e)
            pass

    def __make_exam(self, exam_data: dict) -> Exam | None:
        try:
            student_id = exam_data.get("student_identification")
            template_id = exam_data.get("template_id")
            group_id = exam_data.get("group_id")
            student_name = exam_data.get("student_name")
            binary_data = exam_data.get("exam_binary") or b""
            filename = exam_data.get("filename", "exam")

            if (
                group_id is None
                or student_id is None
                or template_id is None
                or student_name is None
            ):
                return
            if not isinstance(template_id, str):
                template_id = str(template_id)

            # Obtener información del grupo
            group = self.group_repo.get_group_by_id(group_id)
            if group is None:
                return

            # Generar nombre único para el archivo en storage
            file_extension = self.__get_file_extension_from_binary(
                binary_data, filename
            )
            cloud_storage_path = (
                f"exams/{group_id}/{template_id}/{student_id}{file_extension}"
            )

            # Subir a storage (MinIO o GCP según STORAGE_PROVIDER)
            if not binary_data:
                return

            storage_url = self.storage_repo.upload_binary(
                binary_data=binary_data,
                destination_blob_name=cloud_storage_path,
                content_type=self.__get_content_type(file_extension),
            )

            if storage_url is None:
                return

            return Exam(
                group_id=group_id,
                student_identification=int(student_id),
                status="pending",
                exam_path=storage_url,
                template_id=template_id,
                student_name=student_name,
                group_name=group.name,
                period=group.period,
                professor_id=group.professor_id,
            )
        except Exception as e:
            raise ValueError(f"Error creating exam: {str(e)}") from e

    def __get_file_extension_from_binary(
        self, binary_data: bytes, filename: str
    ) -> str:
        """
        Get file extension from filename or infer from binary data
        """
        # Try to get extension from filename first
        if filename and "." in filename:
            return "." + filename.split(".")[-1].lower()

        # Inferir extensión basado en los primeros bytes (magic numbers)
        if binary_data:
            if binary_data.startswith(b"\xff\xd8\xff"):
                return ".jpg"
            elif binary_data.startswith(b"\x89PNG\r\n\x1a\n"):
                return ".png"
            elif binary_data.startswith(b"%PDF"):
                return ".pdf"

        return ".bin"  # Default extension

    def __get_content_type(self, file_extension: str) -> str:
        """
        Get MIME content type based on file extension
        """
        content_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".pdf": "application/pdf",
            ".bin": "application/octet-stream",
        }
        return content_types.get(file_extension.lower(), "application/octet-stream")

    def get_exams_by_template(self, template_id: str) -> list[Exam]:
        return self.exam_repo.get_exams_by_template(template_id)
