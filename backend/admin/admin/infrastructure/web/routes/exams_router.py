import os
import time
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, HTTPException, UploadFile, status
from fastapi.params import Depends, Form

from admin.di import get_exam_usecase
from admin.domain.manager.entities.exams import Exam
from admin.domain.manager.usecases.exams_usecase import IExamsUsecase

exams_router = APIRouter(tags=["Exams router"])


@exams_router.post("/exam", status_code=status.HTTP_201_CREATED)
async def create_exam(
    file: UploadFile,
    student_id: Annotated[str, Form()],
    template_response_id: Annotated[str, Form()],
    group_id: Annotated[str, Form()],
    student_name: Annotated[str, Form()],
    usecase: Annotated[IExamsUsecase, Depends(get_exam_usecase)],
) -> Exam:
    # Leer el contenido del archivo como bytes
    file_content = await file.read()

    # Siempre usar storage (MinIO o GCP según STORAGE_PROVIDER)
    # El usecase se encarga de subir el archivo
    request = {
        "student_identification": student_id,
        "template_id": template_response_id,
        "group_id": group_id,
        "student_name": student_name,
        "exam_binary": file_content,
        "filename": file.filename or f"upload_{int(time.time())}",
    }

    exam = await usecase.create_exam(request)

    if exam is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return exam


@exams_router.get("/exams", description="Useful to get all exams by template")
async def delete_template(
    template_id: str,
    usecase: Annotated[IExamsUsecase, Depends(get_exam_usecase)],
):
    exams = usecase.get_exams_by_template(template_id)
    if len(exams) == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return exams
