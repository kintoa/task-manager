from pydantic import BaseModel, ConfigDict
from .status import TaskStatus
from typing import Optional


class TaskSchema(BaseModel):
    uuid: str
    title: str
    description: str
    status: TaskStatus


class TaskUpdateInputSchema(BaseModel):
    uuid: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskResponseSchema(BaseModel):
    id: int
    uuid: str
    title: str
    description: str
    status: str

    model_config = ConfigDict(from_attributes=True)
