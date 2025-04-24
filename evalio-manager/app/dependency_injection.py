from domain.templates.groups_usecase import GroupUsecase
from domain.templates.templates_usecase import TemplateUsecase
from infrastructure.database.mongo_imp import Mongo
from fastapi import Depends

from infrastructure.database.repositories.group_repo import GroupRepository
from infrastructure.database.repositories.template_repo import TemplateResponsesRepository


async def get_mongo():
    return Mongo()


async def get_group_repo(mongo=Depends(get_mongo)):
    return GroupRepository(mongo=mongo)


async def get_template_repo(mongo=Depends(get_mongo)):
    return TemplateResponsesRepository(mongo)


async def get_template_usecase(group_repo=Depends(get_group_repo), template_repo=Depends(get_template_repo)):
    return TemplateUsecase(group_repo=group_repo, template_repo=template_repo)


async def get_group_usecase(group_repo=Depends(get_group_repo)):
    return GroupUsecase(group_db=group_repo)
