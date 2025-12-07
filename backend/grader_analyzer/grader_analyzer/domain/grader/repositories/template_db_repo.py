from abc import ABC, abstractmethod

from bson import ObjectId

from grader_analyzer.domain.grader.entities.templates import TemplateResponses
from grader_analyzer.infrastructure.database.mongo_imp import Mongo

COLLECTION_TEMPLATES = "template_responses"


class ITemplateDBRepository(ABC):
    @abstractmethod
    def get_template(self, template_id: str) -> TemplateResponses | None:
        pass


class TemplateRepository(ITemplateDBRepository):
    def __init__(self, mongo: Mongo):
        self.collection = mongo.db.get_collection(COLLECTION_TEMPLATES)

    def get_template(self, template_id: str) -> TemplateResponses | None:
        try:
            exam = self.collection.find_one({"_id": ObjectId(template_id)})
            if exam:
                return TemplateResponses(**exam)
        except Exception as e:
            raise Exception(f"error fetching template {str(e)}") from e
