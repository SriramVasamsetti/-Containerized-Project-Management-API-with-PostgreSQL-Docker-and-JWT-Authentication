from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.models.task import Task
from src.repositories.task_repository import TaskRepository
from src.services.project_service import ProjectService
from src.schemas.task import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, db: Session):
        self.task_repo = TaskRepository(db)
        self.project_service = ProjectService(db)

    def create_task(self, project_id: int, data: TaskCreate, owner_id: int) -> Task:
        # Validate project ownership first
        self.project_service.get_project_by_id(project_id, owner_id)
        
        task = Task(
            title=data.title,
            description=data.description,
            status=data.status,
            due_date=data.due_date,
            project_id=project_id
        )
        return self.task_repo.create(task)

    def get_tasks_by_project(self, project_id: int, owner_id: int) -> List[Task]:
        # Validate project ownership first
        self.project_service.get_project_by_id(project_id, owner_id)
        return self.task_repo.get_all_by_project(project_id)

    def get_task_by_id(self, task_id: int, owner_id: int) -> Task:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        # Validate ownership through parent project
        self.project_service.get_project_by_id(task.project_id, owner_id)
        return task

    def update_task(self, task_id: int, data: TaskUpdate, owner_id: int) -> Task:
        task = self.get_task_by_id(task_id, owner_id)
        
        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.status is not None:
            task.status = data.status
        if data.due_date is not None:
            task.due_date = data.due_date
            
        return self.task_repo.update(task)

    def delete_task(self, task_id: int, owner_id: int) -> None:
        task = self.get_task_by_id(task_id, owner_id)
        self.task_repo.delete(task)
