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
                      ) -> Exam:

    # Leer el contenido del archivo como bytes
    file_content = await file.read()
    
    # Determinar si estamos en modo local o producción
    environment = os.getenv("ENVIRONMENT", "local")
    
    if environment == "local":
        # Modo local: guardar archivo temporalmente
        file_location = f"shared/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(file_content)
        
        request = {
            "student_identification": student_id,
            "template_id": template_response_id,
            "group_id": group_id,
            "student_name": student_name,
            "exam_path": str(file_location),
        }
    else:
        # Modo producción: enviar datos binarios directamente
        request = {
            "student_identification": student_id,
            "template_id": template_response_id,
            "group_id": group_id,
            "student_name": student_name,
            "exam_binary": file_content,
        }
    
    exam = await usecase.create_exam(request)
    
    
    if exam is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return exam


@exams_router.get("/exams", description="Useful to get all exams by template")
async def delete_template(template_id: str,  usecase: Annotated[IExamsUsecase, Depends(get_exam_usecase)],
                          ):
    exams = usecase.get_exams_by_template(template_id)
    if len(exams) == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return exams
