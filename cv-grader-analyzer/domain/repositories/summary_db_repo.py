from abc import ABC, abstractmethod

from domain.entities.summary_qualifications import SummaryQualifications


class ISumaryRepository(ABC):

    @abstractmethod
    def update_summary_qualification(self, summary_qualification: SummaryQualifications):
        pass