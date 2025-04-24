from abc import ABC, abstractmethod
from typing import List

from domain.templates.entities.group import Group


class IGroupDbRepo(ABC):

    @abstractmethod
    def get_group(self, group_name: str, professor_id: str, period: str) -> Group | None:
        pass

    @abstractmethod
    def create_group(self, group: Group) -> bool:
        pass

    @abstractmethod
    def get_groups(self, professor_id:str)-> List[Group]:
        pass

    @abstractmethod
    def delete_group(self, professor_id: str, group_name: str, period: str):
        pass