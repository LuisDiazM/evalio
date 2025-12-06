from abc import ABC, abstractmethod

from admin.domain.manager.entities.summary_qualifications import SummaryQualifications
from admin.infrastructure.database.mongo_imp import Mongo

SUMMARY_COLLECTION = "summary_qualifications"


class ISummaryQualificationsRepository(ABC):
    @abstractmethod
    def get_qualification_by_template(
        self, template_id: str
    ) -> SummaryQualifications | None:
        pass

    @abstractmethod
    def delete_qualification_by_group(self, group_id: str) -> None:
        pass


class SummaryQualificationsRepository(ISummaryQualificationsRepository):
    def __init__(self, mongo: Mongo):
        self.coll = mongo.db.get_collection(SUMMARY_COLLECTION)

    def get_qualification_by_template(
        self, template_id: str
    ) -> SummaryQualifications | None:
        try:
            result = self.coll.find_one({"template_id": template_id})
            if result is None:
                return
            return SummaryQualifications(id=str(result.get("_id")), **result)
        except Exception as e:
            raise ValueError(f"error getting qualification {str(e)}") from e

    def delete_qualification_by_group(self, group_id: str) -> None:
        try:
            self.coll.delete_one({"group_id": group_id})
        except Exception as e:
            raise ValueError(f"error deleting qualification by group {str(e)}") from e
