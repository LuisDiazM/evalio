from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, Header, Path, UploadFile, status
import shutil
import os
from app.dependency_injection import get_exam_usecase
from domain.templates.entities.exams import Exam
from domain.templates.exams_usecase import IExamsUsecase


exams_router = APIRouter(
    tags=["Exams router"]
)


@exams_router.post("/exam", status_code=status.HTTP_201_CREATED)
async def create_exam(file: UploadFile,
                      student_id: Annotated[str, Form()],
                      template_response_id: Annotated[str, Form()],
                      group_id: Annotated[str, Form()],
                      student_name: Annotated[str, Form()],
                      usecase: Annotated[IExamsUsecase, Depends(get_exam_usecase)],
                      professor_id: str = Header(None)) -> Exam:

    file_location = f"shared/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    request = {
        "student_identification": student_id,
        "template_id": template_response_id,
        "group_id": group_id,
        "student_name": student_name,
        "exam_path": str(file_location),
    }
    exam = await usecase.create_exam(request)
    if os.getenv("ENVIRONMENT") == "cloud":
        try:
            os.remove(file_location)
        except Exception as e:
            print(f"Error deleting file: {str(e)}")
    if exam is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return exam


@exams_router.get("/exams", description="Useful to get all exams by template")
async def delete_template(template_id: str,  usecase: Annotated[IExamsUsecase, Depends(get_exam_usecase)],
                          professor_id: str = Header(None)):
    exams = usecase.get_exams_by_template(template_id)
    if len(exams) == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return exams
