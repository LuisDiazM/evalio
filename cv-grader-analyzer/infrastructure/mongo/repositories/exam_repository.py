from bson import ObjectId
from domain.entities.exams import Exam
from domain.repositories.exam_db_repo import IExamRepository
from infrastructure.mongo.mongo import MongoDB


class ExamRepository(IExamRepository):
    def __init__(self, mongo: MongoDB):
        client = mongo.client
        if not client:
            raise ValueError("MongoDB client is not initialized.")
        db = client.get_database("manager")
        self.coll = db.get_collection("exams")

    def get_exam_by_id(self, exam_id: str) -> Exam | None:
        try:
            exam = self.coll.find_one({"_id": ObjectId(exam_id)})
            if exam:
                exam["id"] = str(exam["_id"])
                return Exam(**exam)
        except Exception as e:
            raise Exception(f"error fetching exam {str(e)}")

    def update_exam(self, exam_id: str, update_data: dict):
        try:
            self.coll.update_one({"_id": ObjectId(exam_id)}, {"$set": update_data})
        except Exception as e:
            raise Exception(f"error upgrading exam {exam_id} --> {str(e)}")
