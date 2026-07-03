from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from src.models.task import TaskStatus

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=150, description="Task title cannot be empty")
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    due_date: Optional[datetime]
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
