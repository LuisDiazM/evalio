from typing import Annotated
from fastapi import APIRouter, Depends, Header, Response, HTTPException, status
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
async def generate_template(group_id: str,  template_id: str,
                            usecase: Annotated[ITemplatesUsecase, Depends(get_template_usecase)]):

    input_usecase = InputGenTemplate(
        group_id=group_id, template_id=template_id)
    template_temp = usecase.generate_template(input_usecase)
    if template_temp == "":
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    template_path = Path(template_temp)
    if template_path.exists():
        content = template_path.read_bytes()
        os.remove(template_temp)
        return Response(
            content=content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={group_id}-template.pdf"}
        )


@template_router.post("/template", description="Useful to create a template for response sheets")
async def create_template(template: TemplateResponses,
                          usecase: Annotated[ITemplatesUsecase, Depends(get_template_usecase)],
                          professor_id: str = Header(None),):
    temp = template.model_copy()
    temp.professor_id = professor_id
    template_response = usecase.create_template_response(temp)
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
async def get_templates(group_id: str, usecase: Annotated[ITemplatesUsecase, Depends(get_template_usecase)]):
    templates = usecase.get_templates_by_group(group_id)
    if len(templates) > 0:
        return templates
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@template_router.delete("/template", description="Useful to delete a template by Id", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(template_id: str,  usecase: Annotated[ITemplatesUsecase, Depends(get_template_usecase)],
                          professor_id: str = Header(None)):
    usecase.delete_template(template_id)
