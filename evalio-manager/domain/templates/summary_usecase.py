from domain.templates.entities.summary_qualifications import SummaryQualifications
from domain.templates.repositories.db_summary_repo import ISummaryQualificationsRepository
from domain.templates.repositories.storage_repo import IStorageRepository
from abc import ABC, abstractmethod

class ISummaryQualificationsUsecase(ABC):
    @abstractmethod
    def get_summary(self, template_id: str) -> SummaryQualifications | None:
        pass

    @abstractmethod
    def delete_summary(self, group_id:str):
        pass

class SummaryUsecase:
    def __init__(self, db_summary_repo: ISummaryQualificationsRepository, storage_repo: IStorageRepository):
        self.db_summary_repo = db_summary_repo
        self.storage_repo = storage_repo

    def get_summary(self, template_id: str) -> SummaryQualifications | None:
        summary = self.db_summary_repo.get_qualification_by_template(template_id)
        if summary:
            # Generate signed URLs for each student's exam_path
            for student in summary.students:
                if student.exam_path:
                    signed_url = self.storage_repo.generate_signed_url(student.exam_path, expiration_hours=2)
                    if signed_url:
                        student.exam_path = signed_url
            
        return summary

    def delete_summary(self, group_id:str):
        return self.db_summary_repo.delete_qualification_by_group(group_id)