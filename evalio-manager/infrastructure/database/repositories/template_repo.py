from bson import ObjectId
from domain.templates.repositories.db_template_repo import ITemplateRepository
from infrastructure.database.mongo_imp import Mongo
from domain.templates.entities.template_responses import TemplateResponses


class TemplateResponsesRepository(ITemplateRepository):
    def __init__(self, mongo: Mongo):
        self.coll = mongo.db.get_collection("template_responses")

    def create_template_response(self, template_response: TemplateResponses) -> str:
        try:
            data = template_response.model_dump()
            data.pop("id")
            result = self.coll.insert_one(data)
            return str(result.inserted_id)
        except Exception:
            return ""

    def get_template_by_id(self, template_id: str) -> TemplateResponses | None:
        filter = {"_id": ObjectId(template_id)}
        response = self.coll.find_one(filter)
        if response:
            try:
                return TemplateResponses(**response, id=str(response.get("_id")))
            except Exception:
                return

    def get_templates_by_group(self, group_id: str) -> list[TemplateResponses]:
        filter = {"group_id": group_id}
        response = self.coll.find(filter)
        if response:
            try:
                return [TemplateResponses(**template, id=str(template.get("_id"))) for template in response]
            except Exception:
                return []
        return []

    def delete_template_response(self, template_id: str):
        filter = {"_id": ObjectId(template_id)}
        self.coll.delete_one(filter)

    def delete_templates_by_group(self, group_id:str):
        filter = {"group_id": group_id}
        self.coll.delete_many(filter)