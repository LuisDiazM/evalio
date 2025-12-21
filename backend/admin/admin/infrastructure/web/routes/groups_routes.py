import contextlib
from io import BytesIO
from typing import Annotated

import pandas as pd
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)

from admin.di import get_group_usecase
from admin.domain.manager.entities.group import Group, Student
from admin.domain.manager.usecases.groups_usecase import IGroupUsecase
from admin.shared.file_operations import (
    ALLOWED_FORMATS,
    MAX_SIZE,
    validate_columns_csv,
    validate_file,
)

group_router = APIRouter(tags=["groups"])


@group_router.post("/group")
async def create_students_group(
    file: UploadFile,
    name: Annotated[str, Form()],
    period: Annotated[str, Form()],
    subject_name: Annotated[str, Form()],
    usecase: Annotated[IGroupUsecase, Depends(get_group_usecase)],
    request: Request,
):
    professor_id = request.headers.get("x-professor-id") or ""
    professor_name = request.headers.get("x-professor-name") or ""
    if professor_id == "" or professor_name == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing professor ID or name in headers",
        )

    content_type = file.content_type if file.content_type is not None else ""
    file_size = file.size if file.size is not None else 0
    is_valid_file = validate_file(content_type, file_size)
    if not is_valid_file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"only support {ALLOWED_FORMATS} and max {MAX_SIZE} bytes",
        )
    try:
        content = await file.read()
        df = pd.read_csv(BytesIO(content))
        columns = list(df.columns)
        is_valid_csv = validate_columns_csv(columns)
        if not is_valid_csv:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CSV must be have Documento, Nombre as columns",
            )
        students = df.to_dict(orient="records")
        students_grouped = [
            Student(
                **{
                    "name": x.get("Nombre", ""),
                    "identification": x.get("Documento", ""),
                }
            )
            for x in students
        ]
        group = Group(
            name=name,
            period=period,
            subject_name=subject_name,
            professor_id=professor_id,
            professor_name=professor_name,
            students=students_grouped,
        )
        usecase.create(group)
        return group
    except Exception as e:
        # Propagate as HTTPException but keep original message for traceability
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


@group_router.get("/groups", description="get the groups by professor id")
async def get_groups_by_professor(
    usecase: Annotated[IGroupUsecase, Depends(get_group_usecase)], request: Request
) -> list[Group]:
    professor_id = request.headers.get("x-professor-id") or ""
    if professor_id == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing professor ID in headers",
        )
    return usecase.get_groups(professor_id)


@group_router.get("/group", description="get group by id")
async def get_group_by_id(
    id: str,
    usecase: Annotated[IGroupUsecase, Depends(get_group_usecase)],
) -> Group:
    group = usecase.get_group_by_id(group_id=id)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="Group not found"
        )
    return group


@group_router.delete("/group", description="delete an specific group")
async def delete_group(
    group_id: str,
    usecase: Annotated[IGroupUsecase, Depends(get_group_usecase)],
    background_tasks: BackgroundTasks,
    request: Request,
):
    # run deletion in background so HTTP request returns immediately
    professor_id = request.headers.get("x-professor-id") or ""
    if professor_id == "":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing professor ID in headers",
        )

    def _delete():
        with contextlib.suppress(Exception):
            usecase.delete_group(group_id, professor_id)

    background_tasks.add_task(_delete)
    usecase.delete_group(group_id, professor_id)
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
