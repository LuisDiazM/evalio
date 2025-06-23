from typing import List
from domain.templates.entities.exams import Exam
from domain.templates.repositories.db_examp_repo import IExamRepository
from abc import ABC, abstractmethod
import os
from pathlib import Path
import json
from domain.templates.repositories.db_group_repo import IGroupDbRepo
from domain.templates.repositories.logger_repo import LoggerInterface
from domain.templates.repositories.nats_bus import EventPublisher
from domain.templates.repositories.storage_repo import IStorageRepository
import uuid
from datetime import datetime


class IExamsUsecase(ABC):
    @abstractmethod
    async def create_exam(self, exam_data: dict):
        pass

    @abstractmethod
    def get_exams_by_template(self, template_id:str) -> List[Exam]:
        pass

class ExamsUsecase:

    def __init__(self, exam_repo: IExamRepository, 
                 group_repo: IGroupDbRepo,
                 logger_repo: LoggerInterface,
                 event_publisher: EventPublisher,
                 storage_repo: IStorageRepository):
        self.exam_repo = exam_repo
        self.group_repo = group_repo
        self.logger_repo = logger_repo
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
            await self.event_publisher.publish(data=json.dumps({"exam_id": exam_id})) # type: ignore
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
            binary_data = exam_data.get("exam_binary")  # Nuevo campo para datos binarios
            
            if group_id is None or student_id is None or template_id is None or student_name is None:
                return
            if not isinstance(template_id, str):
                template_id = str(template_id)
            
            # Obtener información del grupo
            group = self.group_repo.get_group_by_id(group_id)
            if group is None:
                return
            
            # Generar nombre único para el archivo en cloud storage
            file_extension = self.__get_file_extension(file_location, binary_data)
            cloud_storage_path = f"exams/{group_id}/{template_id}/{student_id}{file_extension}"
            
            if os.getenv("ENVIRONMENT", "local") == "local":
                # Modo local: mantener archivo local
                if file_location is None:
                    return
                location = Path(str(file_location))
                abs_path = os.path.abspath(location)
                if abs_path is None:
                    return
                abs_path = str(abs_path)
            else:
                # Modo producción: subir a cloud storage
                if binary_data is not None:
                    # Subir datos binarios directamente
                    cloud_url = self.storage_repo.upload_binary(
                        binary_data=binary_data,
                        destination_blob_name=cloud_storage_path,
                        content_type=self.__get_content_type(file_extension)
                    )
                elif file_location is not None:
                    # Subir archivo desde ruta local
                    cloud_url = self.storage_repo.upload_file(
                        file_path=file_location,
                        destination_blob_name=cloud_storage_path
                    )
                else:
                    self.logger_repo.error("No file data provided for cloud storage upload")
                    return
                
                if cloud_url is None:
                    self.logger_repo.error("Failed to upload file to cloud storage")
                    return
                
                abs_path = cloud_url
                self.logger_repo.info(f"File uploaded to cloud storage: {abs_path}")
            
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

    def __get_file_extension(self, file_location: str, binary_data: bytes) -> str:
        """
        Get file extension from file location or infer from binary data
        """
        if file_location:
            return Path(file_location).suffix
        elif binary_data:
            # Inferir extensión basado en los primeros bytes (magic numbers)
            if binary_data.startswith(b'\xff\xd8\xff'):
                return '.jpg'
            elif binary_data.startswith(b'\x89PNG\r\n\x1a\n'):
                return '.png'
            elif binary_data.startswith(b'%PDF'):
                return '.pdf'
            else:
                return '.bin'  # Default extension
        return '.bin'

    def __get_content_type(self, file_extension: str) -> str:
        """
        Get MIME content type based on file extension
        """
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.pdf': 'application/pdf',
            '.bin': 'application/octet-stream'
        }
        return content_types.get(file_extension.lower(), 'application/octet-stream')

    def get_exams_by_template(self, template_id:str) -> List[Exam]:
        return self.exam_repo.get_exams_by_template(template_id)