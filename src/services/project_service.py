from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.models.project import Project
from src.repositories.project_repository import ProjectRepository
from src.schemas.project import ProjectCreate, ProjectUpdate

class ProjectService:
    def __init__(self, db: Session):
        self.project_repo = ProjectRepository(db)

    def create_project(self, data: ProjectCreate, owner_id: int) -> Project:
        project = Project(
            name=data.name,
            description=data.description,
            owner_id=owner_id
        )
        return self.project_repo.create(project)

    def get_projects_by_owner(self, owner_id: int) -> List[Project]:
        return self.project_repo.get_all_by_owner(owner_id)

    def get_project_by_id(self, project_id: int, owner_id: int) -> Project:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        if project.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this project"
            )
        return project

    def update_project(self, project_id: int, data: ProjectUpdate, owner_id: int) -> Project:
        project = self.get_project_by_id(project_id, owner_id)
        
        if data.name is not None:
            project.name = data.name
        if data.description is not None:
            project.description = data.description
            
        return self.project_repo.update(project)

    def delete_project(self, project_id: int, owner_id: int) -> None:
        project = self.get_project_by_id(project_id, owner_id)
        self.project_repo.delete(project)
