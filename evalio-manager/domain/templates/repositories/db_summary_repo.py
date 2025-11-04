from abc import ABC, abstractmethod

from domain.templates.entities.summary_qualifications import SummaryQualifications

class ISummaryQualificationsRepository(ABC):

    @abstractmethod
    def get_qualification_by_template(self, template_id: str) -> SummaryQualifications | None:
        pass

    @abstractmethod
    def delete_qualification_by_group(self, group_id: str) -> None:
        pass