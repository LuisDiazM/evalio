from typing import Annotated
from fastapi import APIRouter, Depends, Response, HTTPException, status
from pathlib import Path
import os
from app.dependency_injection import get_template_usecase
from domain.templates.entities.input_group import InputGenTemplate
from domain.templates.entities.template_responses import TemplateResponses
from domain.templates.templates_usecase import ITemplatesUsecase


template_router = APIRouter(
    tags=["Template Manager"]
)


@template_router.get("/template", description="Useful to generate template for response sheets, produce a pdf with the students")
async def generate_template(group_name: str, period: str,
                            professor_id: str, template_id: str,
                            usecase: Annotated[ITemplatesUsecase, Depends(get_template_usecase)]):
    input_usecase = InputGenTemplate(group_name=group_name, period=period,
                                     professor_id=professor_id, template_id=template_id)
    template_temp = usecase.generate_template(input_usecase)
    template_path = Path(template_temp)
    if template_path.exists():
        content = template_path.read_bytes()
        os.remove(template_temp)
        return Response(
            content=content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={group_name}-template.pdf"}
        )
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@template_router.post("/template", description="Useful to create a template for response sheets")
async def create_template(template: TemplateResponses,
                           usecase: Annotated[ITemplatesUsecase, Depends(get_template_usecase)]):
    template_response = usecase.create_template_response(template)
    if template_response:
        return template_response
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@template_router.get("/template/{template_id}", description="Useful to get a template")
async def get_template(template_id: str,
                        usecase: Annotated[ITemplatesUsecase, Depends(get_template_usecase)]):
    template_response = usecase.get_template_by_id(template_id)
    if template_response:
        return template_response
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

@template_router.get("/templates", description="Useful to get all templates by professor")
async def get_templates(professor_id:str, usecase: Annotated[ITemplatesUsecase, Depends(get_template_usecase)]):
    templates = usecase.get_templates_by_professor(professor_id)
    if len(templates)> 0:
        return templates
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
