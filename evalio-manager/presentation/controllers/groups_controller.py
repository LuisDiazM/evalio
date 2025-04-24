from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from io import BytesIO
import pandas as pd

from app.dependency_injection import get_group_usecase
from domain.templates.entities.group import Group, Student
from domain.templates.groups_usecase import IGroupUsecase

ALLOWED_FORMATS = ["text/csv"]
MAX_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_COLUMS = ["Documento", "Nombre"]

group_router = APIRouter(
    tags=["Group Router"]
)


def validate_file(content_type: str, size: int) -> bool:
    return content_type in ALLOWED_FORMATS and size <= MAX_SIZE


def validate_columns_csv(columns: List[str]) -> bool:
    return all(elem in columns for elem in ALLOWED_COLUMS)


@group_router.post("/group")
async def create_students_group(file: UploadFile,
                                name: Annotated[str, Form()],
                                period: Annotated[str, Form()],
                                subject_name: Annotated[str, Form()],
                                professor_id: Annotated[str, Form()],
                                professor_name: Annotated[str, Form()],
                                usecase: Annotated[IGroupUsecase, Depends(get_group_usecase)]):
    is_valid_file = validate_file(file.content_type, file.size)
    if not is_valid_file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"only support {ALLOWED_FORMATS} and max {MAX_SIZE} bytes")
    try:
        content = await file.read()
        df = pd.read_csv(BytesIO(content))
        columns = list(df.columns)
        is_valid_csv = validate_columns_csv(columns)
        if not is_valid_csv:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="CSV must be have Documento, Nombre as columns")
        students = df.to_dict(orient="records")
        students_grouped = [Student(
            **{"name": x.get("Nombre", ""), "identification": x.get("Documento", "")}) for x in students]
        group = Group(name=name, period=period, subject_name=subject_name,
                      professor_id=professor_id,
                      professor_name=professor_name, students=students_grouped)
        usecase.create(group)
        return group
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@group_router.get("/groups", description="get the groups by professor id")
async def get_groups_by_professor(professor_id: str,
                                  usecase: Annotated[IGroupUsecase, Depends(get_group_usecase)]) -> List[Group]:
    return usecase.get_groups(professor_id)


@group_router.delete("/group", description="delete an specific group")
async def delete_group(professor_id: str, period: str, group_name: str,
                       usecase: Annotated[IGroupUsecase, Depends(get_group_usecase)]):
    usecase.delete_group(professor_id=professor_id,
                         group_name=group_name, period=period)
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
