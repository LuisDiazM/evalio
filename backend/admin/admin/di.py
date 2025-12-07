import os

from fastapi import Depends
from nats.aio.client import Client as NATS

from admin.domain.manager.repositories.db_exams_summary_repo import ExamsRepository
from admin.domain.manager.repositories.db_group_repo import GroupRepository
from admin.domain.manager.repositories.db_summary_repo import (
    SummaryQualificationsRepository,
)
from admin.domain.manager.repositories.db_template_repo import (
    TemplateResponsesRepository,
)
from admin.domain.manager.usecases.exams_usecase import ExamsUsecase
from admin.domain.manager.usecases.groups_usecase import GroupUsecase
from admin.domain.manager.usecases.summary_usecase import SummaryUsecase
from admin.domain.manager.usecases.templates_usecase import TemplateUsecase
from admin.infrastructure.database.mongo_imp import Mongo
from admin.infrastructure.messaging.nats_publisher import (
    EVENT_PROCESS_EXAM,
    STREAM_NAME,
    NatsPublisher,
)
from admin.infrastructure.storage.cloud_storage_gcp import GCPStorageRepository


# infrastructure
async def get_mongo():
    return Mongo()


async def get_storage_repo():
    return GCPStorageRepository()


async def get_nats():
    nc = NATS()
    host = os.getenv("NATS_URL")
    if host is None:
        raise ValueError("NATS_URL environment variable is not set")
    await nc.connect(host)
    js = nc.jetstream()

    await js.add_stream(name=STREAM_NAME, subjects=[EVENT_PROCESS_EXAM])
    return NatsPublisher(nc)


# Module-level Depends variables to avoid function calls in default arguments (B008)
get_mongo_dep = Depends(get_mongo)
get_storage_repo_dep = Depends(get_storage_repo)
get_nats_dep = Depends(get_nats)


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


async def get_summary_usecase(
    summary_repo=get_summary_repo_dep,
    storage_repo=get_storage_repo_dep,
):
    return SummaryUsecase(
        db_summary_repo=summary_repo,
        storage_repo=storage_repo,
    )


async def get_exam_usecase(
    exam_repo=get_exam_repo_dep,
    storage_repo=get_storage_repo_dep,
    nats_publisher=get_nats_dep,
    group_repo=get_group_repo_dep,
):
    return ExamsUsecase(
        event_publisher=nats_publisher,
        exam_repo=exam_repo,
        storage_repo=storage_repo,
        group_repo=group_repo,
    )


async def get_template_usecase(
    group_repo=get_group_repo_dep,
    template_repo=get_template_repo_dep,
    storage_repo=get_storage_repo_dep,
    exam_repo=get_exam_repo_dep,
):
    return TemplateUsecase(
        group_repo=group_repo,
        template_repo=template_repo,
        storage_repo=storage_repo,
        exam_repo=exam_repo,
    )
