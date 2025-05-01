from domain.templates.exams_usecase import ExamsUsecase
from domain.templates.groups_usecase import GroupUsecase
from domain.templates.templates_usecase import TemplateUsecase
from infrastructure.database.mongo_imp import Mongo
from fastapi import Depends

from infrastructure.database.repositories.exams_repo import ExamsRepository
from infrastructure.database.repositories.group_repo import GroupRepository
from infrastructure.database.repositories.template_repo import TemplateResponsesRepository
from infrastructure.logger.logger import StandardLogger


async def get_mongo():
    return Mongo()


async def get_logger():
    return StandardLogger()


async def get_group_repo(mongo=Depends(get_mongo)):
    return GroupRepository(mongo=mongo)


async def get_template_repo(mongo=Depends(get_mongo)):
    return TemplateResponsesRepository(mongo)


async def get_exam_repo(mongo=Depends(get_mongo)):
    return ExamsRepository(mongo=mongo)


async def get_template_usecase(group_repo=Depends(get_group_repo),
                               template_repo=Depends(get_template_repo),
                               logger=Depends(get_logger)):
    return TemplateUsecase(group_repo=group_repo, template_repo=template_repo, logger=logger)


async def get_group_usecase(group_repo=Depends(get_group_repo)):
    return GroupUsecase(group_db=group_repo)


async def get_exam_usecase(exam_repo=Depends(get_exam_repo),
                           group_repo=Depends(get_group_repo),
                           logger=Depends(get_logger)):
    return ExamsUsecase(exam_repo=exam_repo, group_repo=group_repo, logger_repo=logger)
