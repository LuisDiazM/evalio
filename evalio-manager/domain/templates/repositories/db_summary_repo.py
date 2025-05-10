from abc import ABC, abstractmethod

from domain.templates.entities.summary_qualifications import SummaryQualifications

class ISummaryQualificationsRepository(ABC):

    @abstractmethod
    def get_qualification_by_group_and_number(self, group_id: str, number: int) -> SummaryQualifications | None:
        pass

    @abstractmethod
    def delete_qualification_by_group_and_number(self, group_id: str, number: int) -> None:
        pass