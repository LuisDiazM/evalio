from abc import ABC, abstractmethod

from admin.domain.manager.entities.exams import Exam
from admin.infrastructure.database.mongo_imp import Mongo

EXAMS_COLLECTION = "exams"


class IExamRepository(ABC):
    @abstractmethod
    def create_exam(self, exam: Exam) -> str | None:
        pass

    @abstractmethod
    def get_exams_by_template(self, template_id: str) -> list[Exam]:
        pass

    @abstractmethod
    def delete_exams_by_template(self, template_id: str):
        pass

    @abstractmethod
    def delete_exams_by_group(self, group_id: str):
        pass


class ExamsRepository(IExamRepository):
    def __init__(self, mongo: Mongo):
        self.coll = mongo.db.get_collection(EXAMS_COLLECTION)

    def create_exam(self, exam: Exam) -> str | None:
        try:
            result = self.coll.find_one(
                {
                    "group_id": exam.group_id,
                    "template_id": exam.template_id,
                    "student_identification": exam.student_identification,
                }
            )
            if result is None:
                resp = self.coll.insert_one(exam.model_dump())
                return str(resp.inserted_id)
            if result.get("status") == "error":
                self.coll.update_one(
                    {"_id": result["_id"]},
                    {"$set": {"status": "pending", "exam_path": exam.exam_path}},
                )
                return str(result["_id"])
        except Exception as e:
            raise ValueError(f"error creating exam {str(e)}") from e

    def get_exams_by_template(self, template_id: str) -> list[Exam]:
        filter = {"template_id": template_id}
        response = self.coll.find(filter)
        if response:
            try:
                return [Exam(**exam) for exam in response]
            except Exception:
                return []
        return []

    def delete_exams_by_template(self, template_id: str):
        try:
            filter = {"template_id": template_id}
            self.coll.delete_many(filter)
        except Exception as e:
            raise ValueError(f"error deleting exams by template {str(e)}") from e

    def delete_exams_by_group(self, group_id: str):
        try:
            filter = {"group_id": group_id}
            self.coll.delete_many(filter)
        except Exception as e:
            raise ValueError(f"error deleting exams by group {str(e)}") from e
