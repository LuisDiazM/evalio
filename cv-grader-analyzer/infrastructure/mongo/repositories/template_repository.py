
from bson import ObjectId
from domain.entities.templates import TemplateResponses
from domain.repositories.template_db_repo import ITemplateDBRepository
from infrastructure.mongo.mongo import MongoDB


class TemplateRepository(ITemplateDBRepository):

    def __init__(self, mongo: MongoDB):
        db = mongo.client.get_database("manager")
        self.collection = db.get_collection("template_responses")

    def get_template(self, template_id: str) -> TemplateResponses | None:
        try:
            exam = self.collection.find_one({"_id": ObjectId(template_id)})
            if exam:
                return TemplateResponses(**exam)
        except Exception as e:
            raise Exception(f"error fetching template {str(e)}")
