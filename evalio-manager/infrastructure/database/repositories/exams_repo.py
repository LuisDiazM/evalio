from domain.templates.entities.exams import Exam
from domain.templates.repositories.db_examp_repo import IExamRepository
from infrastructure.database.mongo_imp import Mongo


class ExamsRepository(IExamRepository):
    def __init__(self, mongo: Mongo):
        self.coll = mongo.db.get_collection("exams")

    def create_exam(self, exam: Exam) -> str | None:
        try:
            result = self.coll.find_one(
                {"group_id": exam.group_id,
                 "template_id": exam.template_id,
                 "student_identification": exam.student_identification}
            )
            if result is None:
                resp = self.coll.insert_one(exam.model_dump())
                return str(resp.inserted_id)
            if result.get("status") == "error":
                self.coll.update_one(
                    {"_id": result["_id"]},
                    {"$set": {"status": "pending", "exam_path": exam.exam_path}}
                )
                return str(result["_id"])
        except Exception as e:
            raise ValueError(f"error creating exam {str(e)}")
