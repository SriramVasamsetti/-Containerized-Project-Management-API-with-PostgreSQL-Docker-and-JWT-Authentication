from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.middleware.auth_dependency import get_current_user
from src.models.user import User
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from src.services.task_service import TaskService

router = APIRouter(tags=["Tasks"])

@router.post("/api/projects/{projectId}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    projectId: int,
    data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task_service = TaskService(db)
    return task_service.create_task(projectId, data, current_user.id)

@router.get("/api/projects/{projectId}/tasks", response_model=List[TaskResponse])
def get_tasks(
    projectId: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task_service = TaskService(db)
    return task_service.get_tasks_by_project(projectId, current_user.id)

@router.get("/api/tasks/{id}", response_model=TaskResponse)
def get_task(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task_service = TaskService(db)
    return task_service.get_task_by_id(id, current_user.id)

@router.put("/api/tasks/{id}", response_model=TaskResponse)
def update_task(
    id: int,
    data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task_service = TaskService(db)
    return task_service.update_task(id, data, current_user.id)

@router.delete("/api/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task_service = TaskService(db)
    task_service.delete_task(id, current_user.id)
    return None
