from abc import ABC, abstractmethod

from domain.entities.templates import TemplateResponses


class ITemplateDBRepository(ABC):
    @abstractmethod
    def get_template(self, template_id: str) -> TemplateResponses | None:
        pass
