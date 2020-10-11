from fastapi import APIRouter, HTTPException
from app.api import crud

from app.schemas import ProjectPayloadSchema, ProjectResponseSchema, ProjectSchema, TaskResponseSchema, TaskPayloadSchema
from app.utils import to_dict

from typing import List

router = APIRouter()


@router.post("/", response_model=ProjectSchema, status_code=201)
async def create_project(payload: ProjectPayloadSchema) -> ProjectSchema:
    project = await crud.post_project(payload)
    return project


@router.get("/", response_model=List[ProjectResponseSchema])
async def get_projects():
    projects = await crud.get_projects()
    return projects


@router.get("/{project_id}", response_model=ProjectSchema)
async def get_project(project_id: int) -> ProjectSchema:
    project = await crud.get_project(project_id)
    if project is None:
        raise HTTPException(404, "This project id does not exist")
    return project


@router.put("/{project_id}", response_model=ProjectSchema)
async def get_project(project_id: int, payload: ProjectPayloadSchema) -> ProjectSchema:
    print(payload)
    project = await crud.put_project(project_id, payload)
    #if project is None:
    #    raise HTTPException(404, "This project id does not exist")
    print (project)
    return project


@router.get("/{project_id}/tasks", response_model=List[TaskResponseSchema])
async def get_project_tasks(project_id: int) -> List[TaskResponseSchema]:
    project = await crud.get_project_tasks(project_id)
    if project is None:
        raise HTTPException(404, "This project id does not exist")
    return project


@router.post("/{project_id}/tasks", response_model=TaskResponseSchema)
async def create_task(project_id: int, payload: TaskPayloadSchema) -> TaskResponseSchema:
    task = await crud.post_task(project_id, payload.name)
    if task is None:
        raise HTTPException(404, "This project id does not exist")
    print("Project", task)
    return task


@router.delete("/{project_id}")
async def delete_project(project_id: int):
    res = await crud.delete_project(project_id)

    print(res)

    return {"message": f"Delete Project {project_id}"}
