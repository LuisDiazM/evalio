from fastapi import Depends

from admin.domain.manager.repositories.db_exams_summary_repo import ExamsRepository
from admin.domain.manager.repositories.db_group_repo import GroupRepository
from admin.domain.manager.repositories.db_summary_repo import (
    SummaryQualificationsRepository,
)
from admin.domain.manager.repositories.db_template_repo import (
    TemplateResponsesRepository,
)
from admin.domain.manager.usecases.groups_usecase import GroupUsecase
from admin.infrastructure.database.mongo_imp import Mongo
from admin.infrastructure.storage.cloud_storage_gcp import GCPStorageRepository


# infrastructure
async def get_mongo():
    return Mongo()


async def get_storage_repo():
    return GCPStorageRepository()


# Module-level Depends variables to avoid function calls in default arguments (B008)
get_mongo_dep = Depends(get_mongo)
get_storage_repo_dep = Depends(get_storage_repo)


# respositories/adapters
async def get_group_repo(mongo=get_mongo_dep):
    return GroupRepository(mongo=mongo)


async def get_template_repo(mongo=get_mongo_dep):
    return TemplateResponsesRepository(mongo=mongo)


async def get_exam_repo(mongo=get_mongo_dep):
    return ExamsRepository(mongo=mongo)


async def get_summary_repo(mongo=get_mongo_dep):
    return SummaryQualificationsRepository(mongo=mongo)


# domain
# Module-level Depends for repo providers (defined after the provider functions)
get_group_repo_dep = Depends(get_group_repo)
get_template_repo_dep = Depends(get_template_repo)
get_exam_repo_dep = Depends(get_exam_repo)
get_summary_repo_dep = Depends(get_summary_repo)


async def get_group_usecase(
    group_repo=get_group_repo_dep,
    template_repo=get_template_repo_dep,
    summary_repo=get_summary_repo_dep,
    exam_repo=get_exam_repo_dep,
    storage_repo=get_storage_repo_dep,
):
    return GroupUsecase(
        group_db=group_repo,
        template_db=template_repo,
        summary_db=summary_repo,
        exam_db=exam_repo,
        storage_repo=storage_repo,
    )
