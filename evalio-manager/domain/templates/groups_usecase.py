from abc import ABC, abstractmethod
from typing import List
import concurrent.futures

from domain.templates.entities.group import Group
from domain.templates.repositories.db_examp_repo import IExamRepository
from domain.templates.repositories.db_group_repo import IGroupDbRepo
from domain.templates.repositories.db_summary_repo import ISummaryQualificationsRepository
from domain.templates.repositories.db_template_repo import ITemplateRepository


class IGroupUsecase(ABC):

    @abstractmethod
    def create(self, group: Group) -> bool:
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


class GroupUsecase(IGroupUsecase):
    def __init__(self, group_db: IGroupDbRepo,
                 template_db: ITemplateRepository,
                 exam_db: IExamRepository,
                 summary_db: ISummaryQualificationsRepository):
        self.group_db = group_db
        self.template_db = template_db
        self.exam_db = exam_db
        self.summary_db = summary_db

    def create(self, group: Group):
        return self.group_db.create_group(group)

    def get_groups(self, professor_id: str):
        return self.group_db.get_groups(professor_id)

    def delete_group(self, group_id: str):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.group_db.delete_group, group_id),
                executor.submit(
                    self.template_db.delete_templates_by_group, group_id),
                executor.submit(self.exam_db.delete_exams_by_group, group_id),
                executor.submit(
                    self.summary_db.delete_qualification_by_group, group_id)
            ]
            concurrent.futures.wait(futures)

    def get_group_by_id(self, group_id: str):
        return self.group_db.get_group_by_id(group_id)
