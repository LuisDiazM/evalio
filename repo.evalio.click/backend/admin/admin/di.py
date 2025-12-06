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
from fastapi import Depends


# infrastructure
async def get_mongo():
    return Mongo()


async def get_storage_repo():
    return GCPStorageRepository()


# respositories/adapters
async def get_group_repo(mongo=Depends(get_mongo)):
    return GroupRepository(mongo=mongo)


async def get_template_repo(mongo=Depends(get_mongo)):
    return TemplateResponsesRepository(mongo)


async def get_exam_repo(mongo=Depends(get_mongo)):
    return ExamsRepository(mongo=mongo)


async def get_summary_repo(mongo=Depends(get_mongo)):
    return SummaryQualificationsRepository(mongo)


# domain
async def get_group_usecase(
    group_repo=Depends(get_group_repo),
    template_repo=Depends(get_template_repo),
    summary_repo=Depends(get_summary_repo),
    exam_repo=Depends(get_exam_repo),
    storage_repo=Depends(get_storage_repo),
):
    return GroupUsecase(
        group_db=group_repo,
        template_db=template_repo,
        summary_db=summary_repo,
        exam_db=exam_repo,
        storage_repo=storage_repo,
    )
