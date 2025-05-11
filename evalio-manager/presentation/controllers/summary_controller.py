
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException

from app.dependency_injection import get_summary_usecase
from domain.templates.summary_usecase import ISummaryQualificationsUsecase


summary_router = APIRouter(
    tags=["Summary Router"]
)


@summary_router.get("/summary", description="Useful to get a summary qualifications consolidated by group and exams")
async def get_summary(group_id: str,
                      usecase: Annotated[ISummaryQualificationsUsecase, Depends(get_summary_usecase)]):
    summary = usecase.get_summary(group_id=group_id)
    if summary:
        return summary
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
