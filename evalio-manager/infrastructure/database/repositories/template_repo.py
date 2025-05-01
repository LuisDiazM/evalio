from bson import ObjectId
from domain.templates.repositories.db_template_repo import ITemplateRepository
from infrastructure.database.mongo_imp import Mongo
from domain.templates.entities.template_responses import TemplateResponses


class TemplateResponsesRepository(ITemplateRepository):
    def __init__(self, mongo: Mongo):
        self.coll = mongo.db.get_collection("template_responses")

    def create_template_response(self, template_response: TemplateResponses) -> str:
        try:
            result = self.coll.insert_one(template_response.model_dump())
            return str(result.inserted_id)
        except Exception:
            return ""

    def get_template_by_id(self, template_id: str) -> TemplateResponses | None:
        filter = {"_id": ObjectId(template_id)}
        response = self.coll.find_one(filter)
        if response:
            try:
                return TemplateResponses(**response)
            except Exception:
                return

    def get_templates_by_professor(self, professor_id: str) -> list[TemplateResponses]:
        filter = {"professor_id": professor_id}
        response = self.coll.find(filter)
        if response:
            try:
                return [TemplateResponses(**template) for template in response]
            except Exception:
                return []
        return []

    def delete_template_response(self, template_id: str):
        filter = {"_id": ObjectId(template_id)}
        self.coll.delete_one(filter)
