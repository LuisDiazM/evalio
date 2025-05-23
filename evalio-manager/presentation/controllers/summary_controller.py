
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException

from app.dependency_injection import get_summary_usecase
from domain.templates.summary_usecase import ISummaryQualificationsUsecase
from fastapi.responses import StreamingResponse
import csv
import io


summary_router = APIRouter(
    tags=["Summary Router"]
)


@summary_router.get("/summary", description="Useful to get a summary qualifications consolidated by templat")
async def get_summary(template_id: str,
                      usecase: Annotated[ISummaryQualificationsUsecase, Depends(get_summary_usecase)]):
    summary = usecase.get_summary(template_id=template_id)
    if summary:
        return summary
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@summary_router.get("/summary/export", description="Export students summary as CSV")
async def export_summary_csv(template_id: str,
                             usecase: Annotated[ISummaryQualificationsUsecase, Depends(get_summary_usecase)]):
    summary = usecase.get_summary(template_id=template_id)
    if not summary or not hasattr(summary, "students"):
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    students = summary.students

    if not students:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    summary_dict = summary.model_dump()
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=students[0].model_dump().keys())
    writer.writeheader()
    writer.writerows(summary_dict.get("students", []))
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=students_summary.csv"}
    )
