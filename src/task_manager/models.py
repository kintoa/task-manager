from sqlmodel import Field, SQLModel
from .status import TaskStatus


class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    uuid: str = Field(max_length=255)
    title: str = Field(max_length=255)
    description: str = Field(max_length=255)
    status: TaskStatus = Field(sa_column_kwargs={"nullable": False})

    __tablename__ = "task"
