from abc import ABC, abstractmethod

from bson import ObjectId

from grader_analyzer.domain.grader.entities.exams import Exam
from grader_analyzer.infrastructure.database.mongo_imp import Mongo

COLLECTION_EXAMS = "exams"


class IExamRepository(ABC):
    @abstractmethod
    def get_exam_by_id(self, exam_id: str) -> Exam | None:
        pass

    @abstractmethod
    def update_exam(self, exam_id: str, update_data: dict):
        pass


class ExamRepository(IExamRepository):
    def __init__(self, mongo: Mongo):
        self.coll = mongo.db.get_collection(COLLECTION_EXAMS)

    def get_exam_by_id(self, exam_id: str) -> Exam | None:
        try:
            exam = self.coll.find_one({"_id": ObjectId(exam_id)})
            if exam:
                exam["id"] = str(exam["_id"])
                return Exam(**exam)
        except Exception as e:
            raise Exception(f"error fetching exam {str(e)}") from e

    def update_exam(self, exam_id: str, update_data: dict):
        try:
            self.coll.update_one({"_id": ObjectId(exam_id)}, {"$set": update_data})
        except Exception as e:
            raise Exception(f"error upgrading exam {exam_id} --> {str(e)}") from e
