import concurrent.futures
from abc import ABC, abstractmethod

from admin.domain.manager.entities.group import Group
from admin.domain.manager.repositories.db_exams_summary_repo import IExamRepository
from admin.domain.manager.repositories.db_group_repo import IGroupDbRepo
from admin.domain.manager.repositories.db_summary_repo import (
    ISummaryQualificationsRepository,
)
from admin.domain.manager.repositories.db_template_repo import ITemplateRepository
from admin.domain.shared.storage_repo import IStorageRepository


class IGroupUsecase(ABC):
    @abstractmethod
    def create(self, group: Group) -> bool:
        pass

    @abstractmethod
    def get_groups(self, professor_id: str) -> list[Group]:
        pass

    @abstractmethod
    def delete_group(self, group_id: str):
        pass

    @abstractmethod
    def get_group_by_id(self, group_id: str) -> Group | None:
        pass


class GroupUsecase(IGroupUsecase):
    def __init__(
        self,
        group_db: IGroupDbRepo,
        template_db: ITemplateRepository,
        exam_db: IExamRepository,
        summary_db: ISummaryQualificationsRepository,
        storage_repo: IStorageRepository,
    ):
        self.group_db = group_db
        self.template_db = template_db
        self.exam_db = exam_db
        self.summary_db = summary_db
        self.storage_repo = storage_repo

    def create(self, group: Group):
        return self.group_db.create_group(group)

    def get_groups(self, professor_id: str):
        return self.group_db.get_groups(professor_id)

    def get_group_by_id(self, group_id: str):
        return self.group_db.get_group_by_id(group_id)

    def delete_group(self, group_id: str):
        templates = self.template_db.get_templates_by_group(group_id)
        for template in templates:
            self.storage_repo.delete_folder(f"exams/{group_id}/{template.id}")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.group_db.delete_group, group_id),
                executor.submit(self.template_db.delete_templates_by_group, group_id),
                executor.submit(self.exam_db.delete_exams_by_group, group_id),
                executor.submit(
                    self.summary_db.delete_qualification_by_group, group_id
                ),
            ]
            concurrent.futures.wait(futures)
