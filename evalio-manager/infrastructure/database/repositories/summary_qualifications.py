
from domain.templates.entities.summary_qualifications import SummaryQualifications
from domain.templates.repositories.db_summary_repo import ISummaryQualificationsRepository
from infrastructure.database.mongo_imp import Mongo


class SummaryQualificationsRepository(ISummaryQualificationsRepository):
    def __init__(self, mongo: Mongo):
        self.coll = mongo.db.get_collection("summary_qualifications")

    def get_qualification_by_group(self, group_id: str) -> SummaryQualifications | None:
        try:
            result = self.coll.find_one(
                {"group_id": group_id}
            )
            if result is None:
                return
            return SummaryQualifications( id=str(result.get("_id")), **result)
        except Exception as e:
            raise ValueError(f"error getting qualification {str(e)}")

    def delete_qualification_by_group(self, group_id: str) -> None:
        try:
            self.coll.delete_one(
                {"group_id": group_id}
            )
        except Exception as e:
            pass