from abc import ABC, abstractmethod

from grader_analyzer.domain.grader.entities.summary_qualifications import (
    SummaryQualifications,
)
from grader_analyzer.infrastructure.database.mongo_imp import Mongo

SUMMARY_COLLECTION = "summary_qualifications"


class ISumaryRepository(ABC):
    @abstractmethod
    def update_summary_qualification(
        self, summary_qualification: SummaryQualifications
    ) -> SummaryQualifications:
        pass


class SummaryQualificationRepository(ISumaryRepository):
    def __init__(self, mongo: Mongo):
        self.collection = mongo.db.get_collection(SUMMARY_COLLECTION)

    def update_summary_qualification(
        self, summary_qualification: SummaryQualifications
    ):
        try:
            result = self.collection.update_one(
                {
                    "group_id": summary_qualification.group_id,
                    "number": summary_qualification.number,
                },
                {
                    "$push": {
                        "students": summary_qualification.students[0].model_dump()
                    },
                    "$set": {"updated_at": summary_qualification.updated_at},
                },
                upsert=False,
            )
            if result.matched_count == 0:
                self.collection.insert_one(summary_qualification.model_dump())

            return summary_qualification
        except Exception as e:
            raise Exception(f"summary qualification: {e}") from e
