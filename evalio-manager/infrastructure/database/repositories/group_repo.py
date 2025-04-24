from typing import List
from domain.templates.entities.group import Group
from domain.templates.repositories.db_group_repo import IGroupDbRepo
from infrastructure.database.mongo_imp import Mongo


class GroupRepository(IGroupDbRepo):
    def __init__(self, mongo: Mongo):
        self.coll = mongo.db.get_collection("groups")

    def get_group(self, group_name: str, professor_id: str, period: str) -> Group | None:
        result = self.coll.find_one(
            {"name": group_name, "period": period, "professor_id": professor_id})
        if result:
            try:
                return Group(**result)
            except Exception:
                return
        return

    def create_group(self, group: Group) -> bool:
        try:
            result = self.coll.find_one_and_update(
                {"name": group.name, "period": group.period, "professor_id": group.professor_id}, {"$set": group.model_dump()})
            if result is None:
                self.coll.insert_one(group.model_dump())
            return True
        except Exception as e:
            return False

    def get_groups(self, professor_id: str) -> List[Group]:
        try:
            cursor = self.coll.find({"professor_id": professor_id})
            results = []
            for data in cursor:
                results.append(Group(**data))
            return results
        except Exception as e:
            return []

    def delete_group(self, professor_id: str, group_name: str, period: str):
        self.coll.delete_one(
            {"professor_id": professor_id, "name": group_name, "period": period})
