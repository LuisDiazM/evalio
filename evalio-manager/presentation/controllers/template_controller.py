from typing import Annotated
from fastapi import APIRouter, Depends, Response, HTTPException, status
from pathlib import Path
import os
from app.dependency_injection import get_template_usecase
from domain.templates.entities.input_group import InputGenTemplate
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
    template_temp = usecase.execute(input_usecase)
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