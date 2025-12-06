from abc import ABC, abstractmethod
from typing import List

from admin.domain.manager.entities.group import Group
from admin.infrastructure.database.mongo_imp import Mongo
from bson import ObjectId

GROUPS_COLLECTION = "groups"


class IGroupDbRepo(ABC):
    @abstractmethod
    def get_group(self, group_id: str, professor_id: str, period: str) -> Group | None:
        pass

    @abstractmethod
    def create_group(self, group: Group) -> bool:
        pass

    @abstractmethod
    def get_groups(self, professor_id: str) -> List[Group]:
        pass

    @abstractmethod
    def delete_group(self, group_id: str):
        pass

    @abstractmethod
    def get_group_by_id(self, group_id: str) -> Group | None:
        pass


class GroupRepository(IGroupDbRepo):
    def __init__(self, mongo: Mongo):
        self.coll = mongo.db.get_collection(GROUPS_COLLECTION)

    def get_group(self, group_id: str, professor_id: str, period: str) -> Group | None:
        result = self.coll.find_one(
            {"name": group_id, "period": period, "professor_id": professor_id}
        )
        if result:
            try:
                return Group(**result)
            except Exception:
                pass
        return

    def create_group(self, group: Group) -> bool:
        try:
            data = group.model_dump()
            data.pop("id")
            result = self.coll.find_one_and_update(
                {
                    "name": group.name,
                    "period": group.period,
                    "professor_id": group.professor_id,
                },
                {"$set": data},
            )
            if result is None:
                self.coll.insert_one(data)
            return True
        except Exception as e:
            return False

    def get_groups(self, professor_id: str) -> List[Group]:
        try:
            cursor = self.coll.find({"professor_id": professor_id})
            results = []
            for data in cursor:
                results.append(Group(id=str(data.get("_id")), **data))
            return results
        except Exception as e:
            return []

    def delete_group(self, group_id: str) -> None:
        self.coll.delete_one({"_id": ObjectId(group_id)})

    def get_group_by_id(self, group_id: str) -> Group | None:
        try:
            result = self.coll.find_one({"_id": ObjectId(group_id)})
            if result:
                return Group(id=str(result.get("_id")), **result)
        except Exception:
            return
