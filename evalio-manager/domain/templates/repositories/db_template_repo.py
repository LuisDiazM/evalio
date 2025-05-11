from abc import ABC, abstractmethod

from domain.templates.entities.template_responses import TemplateResponses


class ITemplateRepository(ABC):
    @abstractmethod
    def create_template_response(self, template_response: TemplateResponses) -> str:
        pass

    @abstractmethod
    def get_template_by_id(self, template_id: str) -> TemplateResponses | None:
        pass

    @abstractmethod
    def get_templates_by_group(self, professor_id: str) -> list[TemplateResponses]:
        pass

    @abstractmethod
    def delete_template_response(self, template_id: str):
        pass
