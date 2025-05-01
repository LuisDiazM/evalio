from domain.entities.summary_qualifications import SummaryQualifications
from domain.repositories.summary_db_repo import ISumaryRepository
from infrastructure.mongo.mongo import MongoDB


class SummaryQualificationRepository(ISumaryRepository):

    def __init__(self, mongo: MongoDB):
        db = mongo.client.get_database("manager")
        self.collection = db.get_collection("summary_qualification")

    def update_summary_qualification(self, summary_qualification: SummaryQualifications):
        try:
            result = self.collection.update_one(
                {"group_id": summary_qualification.group_id,
                    "number": summary_qualification.number},
                {"$push": {"students":
                           summary_qualification.students[0].model_dump()},
                 "$set": {"updated_at": summary_qualification.updated_at}},
                upsert=False
            )
            if result.matched_count == 0:
                self.collection.insert_one(summary_qualification.model_dump())

            return summary_qualification
        except Exception as e:
            raise Exception(f"summary qualification: {e}")
