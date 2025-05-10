from domain.templates.entities.summary_qualifications import SummaryQualifications
from domain.templates.repositories.db_summary_repo import ISummaryQualificationsRepository
from abc import ABC, abstractmethod

class ISummaryQualificationsUsecase(ABC):
    @abstractmethod
    def get_summary(self, group_id: str, number: int) -> SummaryQualifications | None:
        pass

    @abstractmethod
    def delete_summary(self, group_id:str, number:int):
        pass

class SummaryUsecase:
    def __init__(self, db_summary_repo: ISummaryQualificationsRepository):
        self.db_summary_repo = db_summary_repo

    def get_summary(self, group_id: str, number: int) -> SummaryQualifications | None:
        return self.db_summary_repo.get_qualification_by_group_and_number(group_id, number)

    def delete_summary(self, group_id:str, number:int):
        return self.db_summary_repo.delete_qualification_by_group_and_number(group_id, number)