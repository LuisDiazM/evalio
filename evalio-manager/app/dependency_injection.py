from domain.templates.exams_usecase import ExamsUsecase
from domain.templates.groups_usecase import GroupUsecase
from domain.templates.summary_usecase import SummaryUsecase
from domain.templates.templates_usecase import TemplateUsecase
from infrastructure.database.mongo_imp import Mongo
from fastapi import Depends

from infrastructure.database.repositories.exams_repo import ExamsRepository
from infrastructure.database.repositories.group_repo import GroupRepository
from infrastructure.database.repositories.summary_qualifications import SummaryQualificationsRepository
from infrastructure.database.repositories.template_repo import TemplateResponsesRepository
from infrastructure.logger.logger import StandardLogger
from infrastructure.storage.gcp_storage import GCPStorageRepository
from nats.aio.client import Client as NATS
from infrastructure.messaging.const import EVENT_PROCESS_EXAM, STREAM_NAME
from infrastructure.messaging.nats_publisher import NatsPublisher
import os


async def get_nats():
    nc = NATS()
    host = os.getenv("NATS_URL")
    if host is None:
        raise ValueError("NATS_URL environment variable is not set")
    await nc.connect(host)
    js = nc.jetstream()

    await js.add_stream(name=STREAM_NAME, subjects=[EVENT_PROCESS_EXAM])
    return NatsPublisher(nc)


async def get_mongo():
    return Mongo()


async def get_logger():
    return StandardLogger()


async def get_storage_repo(logger=Depends(get_logger)):
    bucket_name = os.getenv("GCP_BUCKET_NAME", "evalio-multimedia-pdn")
    return GCPStorageRepository(logger=logger, bucket_name=bucket_name)


async def get_group_repo(mongo=Depends(get_mongo)):
    return GroupRepository(mongo=mongo)


async def get_template_repo(mongo=Depends(get_mongo)):
    return TemplateResponsesRepository(mongo)


async def get_exam_repo(mongo=Depends(get_mongo)):
    return ExamsRepository(mongo=mongo)


async def get_summary_repo(mongo=Depends(get_mongo)):
    return SummaryQualificationsRepository(mongo)


async def get_template_usecase(group_repo=Depends(get_group_repo),
                               template_repo=Depends(get_template_repo),
                               exams_repo=Depends(get_exam_repo),
                               logger=Depends(get_logger),
                               storage_repo=Depends(get_storage_repo)):
    return TemplateUsecase(group_repo=group_repo, template_repo=template_repo, logger=logger, exam_repo=exams_repo, storage_repo=storage_repo)


async def get_group_usecase(group_repo=Depends(get_group_repo),
                            template_repo=Depends(get_template_repo),
                            exam_repo=Depends(get_exam_repo),
                            summary_repo=Depends(get_summary_repo),
                            storage_repo=Depends(get_storage_repo)):
    return GroupUsecase(group_db=group_repo, template_db=template_repo, exam_db=exam_repo, summary_db=summary_repo, storage_repo=storage_repo)


async def get_exam_usecase(exam_repo=Depends(get_exam_repo),
                           group_repo=Depends(get_group_repo),
                           logger=Depends(get_logger),
                           nats=Depends(get_nats),
                           storage_repo=Depends(get_storage_repo)):
    return ExamsUsecase(exam_repo=exam_repo, group_repo=group_repo, logger_repo=logger, event_publisher=nats, storage_repo=storage_repo)


async def get_summary_usecase(summary_repo=Depends(get_summary_repo), storage_repo=Depends(get_storage_repo)):
    return SummaryUsecase(db_summary_repo=summary_repo, storage_repo=storage_repo)
