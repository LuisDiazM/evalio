from abc import ABC, abstractmethod
from typing import List

from domain.templates.entities.group import Group
from domain.templates.repositories.db_group_repo import IGroupDbRepo


class IGroupUsecase(ABC):

    @abstractmethod
    def create(self, group: Group) -> bool:
        pass

    @abstractmethod
    def get_groups(self, professor_id: str)->List[Group]:
        pass

class GroupUsecase(IGroupUsecase):
    def __init__(self, group_db: IGroupDbRepo):
        self.group_db = group_db

    def create(self, group: Group):
        return self.group_db.create_group(group)

    def get_groups(self, professor_id: str):
        return self.group_db.get_groups(professor_id)
